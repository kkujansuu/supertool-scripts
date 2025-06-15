import os
import sys
import subprocess
import tempfile

from collections import defaultdict
from pprint import pprint

def open_file(filename):
    from gramps.gui.utils import open_file_with_default_application
    open_file_with_default_application(filename, uistate)


def print_result():
    lines = []
    lines.append("digraph {")
    lines.append("graph [rankdir=LR];")
    for name, count in counts.items():
        if name.endswith("ref"):
            shape = "rectangle"
        else:
            shape = "ellipse"
        lines.append(f'"{name}"[label="{name}\n{count}", shape="{shape}"];')
    for (t1,t2), count in sorted(references.items()):
        key = (t1,t2)
        lines.append(f'"{t1}" -> "{t2}"[label="{count}"];')
    lines.append("}")

    tf = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    p = subprocess.Popen(f"dot -Goverlap=scale -T png -o {tf.name}", shell=True, 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (stdout_data,stderr_data) = p.communicate("\n".join(lines).encode("utf-8"))
    open_file(tf.name)


references = defaultdict(int)
counts = defaultdict(int)

def add(n1,n2):
    references[(n1,n2)] += 1
    
def scan_any(name, obj):
    counts[name] += 1
    
    # Common:
    if hasattr(obj,"get_event_ref_list"):
        for ref in obj.get_event_ref_list():
            add(name, "eventref")
            add("eventref", "event")
            scan_any("eventref", ref)
    if hasattr(obj,"get_citation_list"):
        for _ in obj.get_citation_list():
            add(name, "citation")
    if hasattr(obj,"get_note_list"):
        for _ in obj.get_note_list():
            add(name, "note")
    if hasattr(obj,"get_media_list"):
        for ref in obj.get_media_list():
            add(name, "mediaref")
            add("mediaref", "media")
            scan_any("mediaref", ref)
    if hasattr(obj,"get_attribute_list"):
        for attr in obj.get_attribute_list():
            add(name, "attribute")
            scan_any("attribute", attr)
    if hasattr(obj,"get_tag_list"):
        for _ in obj.get_tag_list():
            add(name, "tag")
    if hasattr(obj,"get_url_list"):
        for _ in obj.get_url_list():
            add(name, "url")

    # Citations:
    if name == "citation" and hasattr(obj, "get_reference_handle"):
        if obj.get_reference_handle():
            add(name, "source")

    # Events:
    if hasattr(obj,"get_place_handle"):
        if obj.get_place_handle():
            add(name, "place")
            
    # People:
    if hasattr(obj,"get_primary_name"):
        if obj.get_primary_name():
            add(name, "name")
            scan_any("name", obj.get_primary_name())
        for n in obj.get_alternate_names():
            add(name, "name")
            scan_any("name", n)
        for _ in obj.get_family_handle_list():
            add(name, "family")
        for _ in obj.get_parent_family_handle_list():
            add(name, "family")
        for _ in obj.get_person_ref_list():
            add(name, "person")
            
    # Families:
    if hasattr(obj,"get_child_ref_list"):
        for cref in obj.get_child_ref_list():
            add(name, "childref")
            add("childref", "person")
            scan_any("childref", cref)
            

    # People and Repositories:
    if hasattr(obj,"get_address_list"):
        for addr in obj.get_address_list():
            add(name, "address")
            scan_any("address", addr)
            
    # Places:
    if hasattr(obj,"get_placeref_list"):
        for ref in obj.get_placeref_list():
            add(name, "place")
        for _ in obj.get_alternative_names():
            add(name, "placename")
        add(name, "placename")

    # Sources:
    if hasattr(obj,"get_reporef_list"):
        for ref in obj.get_reporef_list():
            add(name, "reporef")
            add("reporef", "repository")
            scan_any("reporef", ref)


            

def scan_people():
   for person in db.iter_people():
        scan_any("person", person)
            
def scan_families():
   for obj in db.iter_families():
        scan_any("family", obj)

def scan_events():
   for obj in db.iter_events():
        scan_any("event", obj)

def scan_places():
   for obj in db.iter_places():
        scan_any("place", obj)

def scan_citations():
   for obj in db.iter_citations():
        scan_any("citation", obj)

def scan_sources():
   for obj in db.iter_sources():
        scan_any("source", obj)

def scan_repositories():
   for obj in db.iter_repositories():
        scan_any("repository", obj)

def scan_media():
   for obj in db.iter_media():
        scan_any("media", obj)

def scan_notes():
   for obj in db.iter_notes():
        scan_any("note", obj)

def scan_tags():
   for obj in db.iter_tags():
        scan_any("tag", obj)


def generate_graph():
    scan_people()
    scan_families()
    scan_events()
    scan_places()
    scan_citations()
    scan_sources()
    scan_repositories()
    scan_media()
    scan_notes()
    print_result()

