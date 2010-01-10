Non-client-server / networked code, i.e. desktop applications, usually
look something like this:

class App(object):
    def click(self):
        t = Text("Click!")
        self.win.append(t)

    def run(self, tk):
        self.win = tk.root()
        button = Button("Hello")
        button.click = self.click
        self.win.append(t)

rctk.start(App)

rctk attempts to provide a similar framework for webbrowser UI's, where the
webbrowser is mostly used as a "dumb" display (i.e. minimal code in the browser)
and most logic (and event-handling!) is performed on the serverside. This is
achieved by using HTTP as the display network protocol.

Eventhough HTTP is normally used for mostly stateless request/response 
applications, rctk will use longrunning processes on the serverside that
can store data, database connections, socket connections, and so on.

Q&A

Q: Why?
A: Because it's interesting to try - to see if such a framework is usable
   at all. I see no apparent reasons why it shouldn't be, though it will 
   probably not be suitable for mass usage. Programming specific types of
   applications with specific types of interactions should become easier.
Q: Isn't this really inefficient (network-wise)?
A: Possibly. On the other hand, X11, vnc, NX do similar things but with
   much more low-level primitives. rctk uses rich javascript widgets that
   require a lot less network traffic to communicate with the server.
Q: How is this different from any other webtoolkit?
   Other webtoolkits are page based and mostly run in the browser. rctk only
   has the UI / controls run in the browser, all logic and state are on the
   serverside.
Q: How is this different from any other desktop GUI toolkit?
A: Normal desktop GUI toolkits display directly on the local display. rctk
   requires a browser to display its controls.
Q: Any other advantages?
   - It allows you to run GUI's on headless (X-less) servers, embedded devices
   - It allows you to restore graphical sessions (possibly, future feature)

Planning
- decent object model, in python and javascript
- windows
- buttons
- text/form controls
- better design/layout (css)
- dropdowns
- menu

- testing infra

- more async serverside (less logging, not at http level)
- session handling
- UI rebuilding
- browser separation of javascript (UI) toolkit and window protocol
  (should make it possible to replace jquery with something else)

Ideas

- the whole UI is stored serverside, so restoring the UI (after browser close)
  should be possible
- some sort of py3 support?

Small tasks
-----------
- design improvements (standalone prototyping)
- simple widgets: textarea, dropdown, menu
- tests
- refactoring web.py-isms out of main rctk code (make it some sort of plugin)
- optioneel wrap-support in StaticText
- opsplitsen modules (ook js)
- events indirect aanroepen (i.e. handle_click -> self.click()). Nodig?
- clearen van handlers (None assign)
- websockets: http://blog.chromium.org/2009/12/web-sockets-now-available-in-google.html
- unicode support. Shouldn't be hard but needs to be explicitly defined

toolkit.createcomponent -> create task

=======
Side Projects
-------------

"Receiver", less-trivial server implementation. async, socket support,
multi-session, multi processing (dispatching to processes, each app is 
seperate process)

"WM", window-manager like thingy. Allows several apps to run in the same
browser.

"Fake API", tkinter (and other API) bindings

XML UI - xml ui definition, and possibly a UI builder that produces such a
 definition

Issues
------
- allow toolkitoption to poll for work, default nothing
- ignore / warn if append window on root
