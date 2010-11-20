"""Utilities for writing code that runs on Python 2 and 3"""

import sys
import types

__author__ = "Benjamin Peterson <benjamin@python.org>"
__version__ = "1.0b1"


# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
    integer_types = int,
    class_types = type,
    text_type = str
    binary_type = bytes

    MAXSIZE = sys.maxsize
else:
    string_types = basestring,
    integer_types = (int, long)
    class_types = (type, types.ClassType)
    text_type = unicode
    binary_type = str

    MAXSIZE = sys.maxint


def _add_doc(func, doc):
    """Add documentation to a function."""
    func.__doc__ = doc


def _import_module(name):
    """Import module, returning last module in string."""
    __import__(name)
    return sys.modules[name]


class _LazyDescr(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, obj, tp):
        result = self._resolve()
        setattr(obj, self.name, result)
        # This is a bit ugly, but it avoids running this again.
        delattr(tp, self.name)
        return result


class _Module(_LazyDescr):

    def __init__(self, name, old, new=None):
        super(_Module, self).__init__(name)
        if PY3:
            if new is None:
                new = name
            self.mod = new
        else:
            self.mod = old

    def _resolve(self):
        return _import_module(self.mod)


class _Attribute(_LazyDescr):

    def __init__(self, name, old_mod, new_mod, old_attr=None, new_attr=None):
        super(_Attribute, self).__init__(name)
        if PY3:
            if new_mod is None:
                new_mod = name
            self.mod = new_mod
            if new_attr is None:
                if old_attr is None:
                    new_attr = name
                else:
                    new_attr = old_attr
            self.attr = new_attr
        else:
            self.mod = old_mod
            if old_attr is None:
                old_attr = name
            self.attr = old_attr

    def _resolve(self):
        module = _import_module(self.mod)
        return getattr(module, self.attr)



class _MovedItems(types.ModuleType):
    """Lazy loading of moved objects"""


_moved_attributes = [
    _Attribute("cStringIO", "cStringIO", "io", "StringIO"),
    _Attribute("reload_module", "__builtin__", "imp", "reload"),
    _Attribute("reduce", "__builtin__", "functools"),
    _Attribute("StringIO", "StringIO", "io"),
    _Attribute("xrange", "__builtin__", "builtins", "xrange", "range"),

    _Module("builtins", "__builtin__"),
    _Module("configparser", "ConfigParser"),
    _Module("copyreg", "copy_reg"),
    _Module("http_cookiejar", "cookielib", "http.cookiejar"),
    _Module("http_cookies", "Cookie", "http.cookies"),
    _Module("html_entities", "htmlentitydefs", "html.entities"),
    _Module("html_parser", "HTMLParser", "html.parser"),
    _Module("http_client", "httplib", "http.client"),
    _Module("BaseHTTPServer", "BaseHTTPServer", "http.server"),
    _Module("CGIHTTPServer", "CGIHTTPServer", "http.server"),
    _Module("SimpleHTTPServer", "SimpleHTTPServer", "http.server"),
    _Module("cPickle", "cPickle", "pickle"),
    _Module("queue", "Queue"),
    _Module("reprlib", "repr"),
    _Module("socketserver", "SocketServer"),
    _Module("tkinter", "Tkinter"),
    _Module("tkinter_dialog", "Dialog", "tkinter.dialog"),
    _Module("tkinter_filedialog", "FileDialog", "tkinter.filedialog"),
    _Module("tkinter_scrolledtext", "ScrolledText", "tkinter.scrolledtext"),
    _Module("tkinter_simpledialog", "SimpleDialog", "tkinter.simpledialog"),
    _Module("tkinter_tix", "Tix", "tkinter.tix"),
    _Module("tkinter_constants", "Tkconstants", "tkinter.constants"),
    _Module("tkinter_dnd", "Tkdnd", "tkinter.dnd"),
    _Module("tkinter_colorchooser", "tkColorChooser", "tkinter.colorchooser"),
    _Module("tkinter_commondialog", "tkCommonDialog", "tkinter.commondialog"),
    _Module("tkinter_tkfiledialog", "tkFileDialog", "tkinter.filedialog"),
    _Module("tkinter_font", "tkFont", "tkinter.font"),
    _Module("tkinter_messagebox", "tkMessageBox", "tkinter.messagebox"),
    _Module("tkinter_tksimpledialog", "tkSimpleDialog", "tkinter.simpledialog"),
    _Module("urllib_robotparser", "robotparser", "urllib.robotparser"),
    _Module("winreg", "_winreg"),
]
for attr in _moved_attributes:
    setattr(_MovedItems, attr.name, attr)
del attr

moves = sys.modules["six.moves"] = _MovedItems("moves")


if PY3:
    _meth_func = "__func__"
    _meth_self = "__self__"

    _func_code = "__code__"
    _func_defaults = "__defaults__"
else:
    _meth_func = "im_func"
    _meth_self = "im_self"

    _func_code = "func_code"
    _func_defaults = "func_defaults"


if PY3:
    def get_unbound_function(unbound):
        return unbound


    advance_iterator = next

    def callable(obj):
        return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)
else:
    def get_unbound_function(unbound):
        return unbound.im_func


    def advance_iterator(it):
        return it.next()

    callable = callable
_add_doc(get_unbound_function,
         """Get the function out of a possibly unbound function""")


def get_method_function(meth):
    """Get the underlying function of a bound method."""
    return getattr(meth, _meth_func)


def get_method_self(meth):
    """Get the self of a bound method."""
    return getattr(meth, _meth_self)


def get_function_code(func):
    """Get code object of a function."""
    return getattr(func, _func_code)


def get_function_defaults(func):
    """Get defaults of a function."""
    return getattr(func, _func_defaults)


if PY3:
    def b(s):
        return s.encode("latin-1")
    def u(s):
        return s
    import io
    StringIO = io.StringIO
    BytesIO = io.BytesIO
else:
    def b(s):
        return s
    def u(s):
        return unicode(s)
    import StringIO
    StringIO = BytesIO = StringIO.StringIO
_add_doc(b, """Byte literal""")
_add_doc(u, """Text literal""")


if PY3:
    exec_ = eval("exec")


    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value


    print_ = eval("print")


    def with_metaclass(meta, base=object):
        ns = dict(base=base, meta=meta)
        exec_("""class NewBase(base, metaclass=meta):
    pass""", ns)
        return ns["NewBase"]


else:
    def exec_(code, globs=None, locs=None):
        """Execute code in a namespace."""
        if globs is None:
            frame = sys._getframe(1)
            globs = frame.f_globals
            if locs is None:
                locs = frame.f_locals
            del frame
        elif locs is None:
            locs = globs
        exec("""exec code in globs, locs""")


    exec_("""def reraise(tp, value, tb=None):
    raise tp, value, tb
""")


    def print_(*args, **kwargs):
        """The new-style print function."""
        fp = kwargs.pop("file", sys.stdout)
        if fp is None:
            return
        def write(data):
            if not isinstance(data, basestring):
                data = str(data)
            fp.write(data)
        want_unicode = False
        sep = kwargs.pop("sep", None)
        if sep is not None:
            if isinstance(sep, unicode):
                want_unicode = True
            elif not isinstance(sep, str):
                raise TypeError("sep must be None or a string")
        end = kwargs.pop("end", None)
        if end is not None:
            if isinstance(end, unicode):
                want_unicode = True
            elif not isinstance(end, str):
                raise TypeError("end must be None or a string")
        if kwargs:
            raise TypeError("invalid keyword arguments to print()")
        if not want_unicode:
            for arg in args:
                if isinstance(arg, unicode):
                    want_unicode = True
                    break
        if want_unicode:
            newline = unicode("\n")
            space = unicode(" ")
        else:
            newline = "\n"
            space = " "
        if sep is None:
            sep = space
        if end is None:
            end = newline
        for i, arg in enumerate(args):
            if i:
                write(sep)
            write(arg)
        write(end)


    def with_metaclass(meta, base=object):
        class NewBase(base):
            __metaclass__ = meta
        return NewBase


_add_doc(reraise, """Reraise an exception.""")
_add_doc(with_metaclass, """Create a base class with a metaclass""")
