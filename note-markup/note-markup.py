from gi.repository import Gtk
from gramps.gen.lib import StyledTextTag
from gramps.gui.widgets import StyledTextEditor

def get_markup(note):
    for tag in note.get_styledtext().tags:
	    print(tag.name, tag.value, tag.ranges)
#	    s = note.get_styledtext()._string
	    s = note.get()
	    for a,b in tag.ranges:
		    print("-", s[a:b])
		    yield (tag.name, tag.value, (a,b), s[a:b])
		    
def show_note(note):
    grid = Gtk.Grid()
    grid.set_column_spacing(5)
    grid.set_row_spacing(2)
    cb_list = []
    for row, (name, value, range, text) in enumerate(get_markup(note)):
        if not value: value = ""
        cb = Gtk.CheckButton()
        cb.set_active(True)
        lbl_name = Gtk.Label(name)
        lbl_name.set_halign(Gtk.Align.START)
        lbl_value = Gtk.Label(value)
        lbl_value.set_halign(Gtk.Align.START)
        lbl_text = Gtk.Label(text)
        lbl_text.set_halign(Gtk.Align.START)
        grid.attach(cb, 0, row, 1, 1)
        grid.attach(lbl_name, 1, row, 1, 1)
        grid.attach(lbl_value, 2, row, 1, 1)
        grid.attach(lbl_text, 3, row, 1, 1)
        tag = StyledTextTag(name, value, [range])
        cb_list.append((cb, tag))
    if len(cb_list) == 0:
        return
    dlg = Gtk.Dialog()
    dlg.set_title("Note markup")
    c = dlg.get_content_area()
    c.add(Gtk.Label("Note " + note.gramps_id))
    c.add(grid)
    c.pack_start(Gtk.HSeparator(), False, False, 10)
    
    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    texteditor = StyledTextEditor()
    texteditor.set_editable(False)
    texteditor.set_wrap_mode(Gtk.WrapMode.WORD)
    texteditor.set_text(note.get_styledtext())
    scrolledwindow.set_size_request(600, 300)
    scrolledwindow.add(texteditor)
    c.add(scrolledwindow) #, True, True, 0)

    dlg.add_button("Clear markup", 1)
    dlg.add_button("Undo", 6)
    dlg.add_button("Next", 2)
    dlg.add_button("Quit", 3)
    dlg.show_all()
    old_text = None
    old_tags = note.get_styledtext().tags[:]
    while True:
        rsp = dlg.run()
        if rsp == 2:
            break
        if rsp == 6:
            note.get_styledtext().tags = old_tags
            db.commit_note(note, trans)
            texteditor.set_text(note.get_styledtext())
        if rsp == 3:
            dlg.destroy()
            raise RuntimeError("Canceled")
        if rsp == 1:
            tags = []
            for cb, tag in cb_list:
                print(cb.get_active())
                if not cb.get_active():
                    tags.append(tag)
            note.get_styledtext().tags = tags
            db.commit_note(note, trans)
            texteditor.set_text(note.get_styledtext())
    dlg.destroy()
		
