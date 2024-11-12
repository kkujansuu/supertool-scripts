from supertool_engine import PersonProxy

# Code based on the "Not Related" tool

class Finder:
    def __init__(self, db):
        self.db = db
        
    def find_spouse(self, person, family):
        """ find the spouse of a person """
        spouse_handle = None
        if family:
            if person.get_handle() == family.get_father_handle():
                spouse_handle = family.get_mother_handle()
            else:
                spouse_handle = family.get_father_handle()
        return spouse_handle
    
    def findRelatedPeople(self, handle, use_events=False, use_citations=False):
        self.handlesOfPeopleToBeProcessed = {handle}
        self.numberOfPeopleInDatabase = self.db.get_number_of_people()
        self.handlesOfPeopleAlreadyProcessed = set()
        self.handlesOfPeopleNotRelated = set()
        handlemap = {}

        while len(self.handlesOfPeopleToBeProcessed) > 0:
            handle = self.handlesOfPeopleToBeProcessed.pop()

            # see if we've already processed this person
            if handle in self.handlesOfPeopleAlreadyProcessed:
                continue

            person = self.db.get_person_from_handle(handle)

            # if we get here, then we're dealing with someone new
            step()

            # remember that we've now seen this person
            self.handlesOfPeopleAlreadyProcessed.add(handle)
            handlemap[handle] = person.gramps_id

            # we have 4 things to do:  find (1) spouses, (2) parents, siblings(3), and (4) children

            # step 1 -- spouses
            for familyHandle in person.get_family_handle_list():
                family = self.db.get_family_from_handle(familyHandle)
                spouseHandle = self.find_spouse(person, family)
                if spouseHandle:
                    self.handlesOfPeopleToBeProcessed.add(spouseHandle)

            # step 2 -- parents
            for familyHandle in person.get_parent_family_handle_list():
                family = self.db.get_family_from_handle(familyHandle)
                fatherHandle = family.get_father_handle()
                motherHandle = family.get_mother_handle()
                if fatherHandle:
                    self.handlesOfPeopleToBeProcessed.add(fatherHandle)
                if motherHandle:
                    self.handlesOfPeopleToBeProcessed.add(motherHandle)

            # step 3 -- siblings
            for familyHandle in person.get_parent_family_handle_list():
                family = self.db.get_family_from_handle(familyHandle)
                for childRef in family.get_child_ref_list():
                    childHandle = childRef.ref
                    self.handlesOfPeopleToBeProcessed.add(childHandle)

            # step 4 -- children
            for familyHandle in person.get_family_handle_list():
                family = self.db.get_family_from_handle(familyHandle)
                for childRef in family.get_child_ref_list():
                    childHandle = childRef.ref
                    self.handlesOfPeopleToBeProcessed.add(childHandle)

            # step 5 -- event participants
            if use_events:
                for eventRef in person.get_event_ref_list():
                    eventHandle = eventRef.ref
                    for _, handle in db.find_backlink_handles(eventHandle, ['Person']):
                        self.handlesOfPeopleToBeProcessed.add(handle)

            # step 6 -- people having the same citation
            if use_citations:
                for cithandle in person.get_citation_list():
                    citation = self.db.get_citation_from_handle(cithandle)
                    if citation.page == "": continue
                    for _, handle in db.find_backlink_handles(cithandle, ['Person']):
                        self.handlesOfPeopleToBeProcessed.add(handle)

        plist = []
        for handle in self.handlesOfPeopleAlreadyProcessed:
            person = self.db.get_person_from_handle(handle)
            plist.append( (person.gramps_id, handle) )
        return set(plist) 
        
sets = []
all = set((p.gramps_id, p.handle) for p in db.iter_people())
# print("all",len(all))

while all:    
    gid, handle = sorted(all)[0]
    finder = Finder(db)
    related = finder.findRelatedPeople(handle) #, use_events=True, use_citations=True)
    unrelated = all - related
    sets.append((handle,related))
    all = unrelated

# print("----------------------")
result.set_headers(["Number of people", "Sample person ID", "Sample person"])
for handle, related in sets:
    #handle = related.pop()
    #related.add(handle)
    p = db.get_person_from_handle(handle)
    person = PersonProxy(db, handle)
    # print(f"{len(related):10} {person.gramps_id} {person.name}")
    result.add_row([len(related), person.gramps_id, person.name], handle=person.handle)
    
    
    
    
    
    
    
    
    
    
    
    

