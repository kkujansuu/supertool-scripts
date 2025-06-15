import json
import time
import urllib.parse
import urllib.request

from gi.repository import Gtk
from gramps.gui.dialog import OkDialog
from supertool_engine import SupertoolException

# time.sleep(1) # Nominatim has an absolute maximum of 1 request per second

stopped = False
def get_coordinates(p):
    global stopped
    if stopped: return
    name = p.longname
    name = name.replace("Älvsborgs", "Västra Götalands")
    name = name.replace("Skaraborgs", "Västra Götalands")
    
    query = urllib.parse.urlencode({"q": name, "format": "jsonv2", "limit": 10})
    url = f"https://nominatim.openstreetmap.org/search?{query}"
    rsp = urllib.request.urlopen(url).read()
    data = json.loads(rsp)
    # pprint(data)
    if len(data) == 0:
        OkDialog(p.longname, "No places found")
        return
    dlg = Gtk.Dialog()
    dlg.set_title("Get Coordinates for " + p.longname)
    dlg.set_size_request(500, 200)
    content = dlg.get_content_area()
    grid = Gtk.Grid()
    grid.set_column_spacing(10)
    radio = None
    choices = []
    for index, item in enumerate(data):
        row = 2*index
        radio = Gtk.RadioButton.new_with_label_from_widget(radio, item['addresstype'])
        choices.append(radio)
        grid.attach(radio, 1, row, 1, 1)

        lbl_name = Gtk.Label(item['display_name'])
        lbl_name.set_halign(Gtk.Align.START)
        grid.attach(lbl_name, 2, row, 5, 1)

        lat = item['lat']
        lon = item['lon']
        latlon = f"{lat}, {lon}"
        lbl_latlon = Gtk.Label(latlon)
        lbl_latlon.set_halign(Gtk.Align.START)
        #grid.attach(lbl_latlon, 2, row+1, 1, 1)
        
        url = f"https://www.openstreetmap.org/#map=15/{lat}/{lon}"
        link = f"""<a href="{url}">{latlon}</a>"""
        print(link)
        lbl_link = Gtk.Label(use_markup=True, label=link)
        lbl_link.set_halign(Gtk.Align.START)
        grid.attach(lbl_link, 2, row+1, 1, 1)
        
    content.add(grid)
    but1 = dlg.add_button("Accept", 1)
    but1.set_tooltip_text("Update the coordinates for this place. Continue with next place.")

    but2 = dlg.add_button("Skip", 2)
    but2.set_tooltip_text("Do not update the coordinates for this place. Continue with next place.")

    but3 = dlg.add_button("Stop", 3)
    but3.set_tooltip_text("Do not update the coordinates for this place. Skip also all remaining places. Keep any updates for previous places.")

    but4 = dlg.add_button("Abort", 4)
    but4.set_tooltip_text("Abort the operation an undo any changes for all selected places.")

    copyright = Gtk.Label(use_markup=True, label='Coordinate data from <a href="https:://openstreetmap.org/copyright">OpenStreetMap</a>')
    copyright.set_halign(Gtk.Align.START)
    content.pack_end(copyright, False, False, 10)
    content.show_all()

    rsp = dlg.run()

    if rsp == 1:
        for index, choice in enumerate(choices):
            # print(index, choice.get_active())
            if choice.get_active():
                item = data[index]
                lat = item["lat"]
                lon = item["lon"]
                p.obj.set_latitude(lat)
                p.obj.set_longitude(lon)
                db.commit_place(p.obj, trans)
    dlg.destroy()
    if rsp == 3:
        # raise StopIteration()
        stopped = True
    if rsp == 4:
        raise SupertoolException("Canceled")


