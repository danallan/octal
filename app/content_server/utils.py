import config
import database
import graphs

db = None
def load_db():
    global db
    db = database.Database.load(config.CONTENT_PATH)
    
def find_references(key):
    global db
    if db is None:
        load_db()

    if key not in db.nodes:
        print 'Not found.'
        return

    print 'The following concepts depend on it:'
    for tag, node in db.nodes.items():
        for dep in node.dependencies:
            if dep.tag == key:
                print '   ', tag

    print 'The following shortcuts depend on it:'
    for tag, shortcut in db.shortcuts.items():
        for dep in shortcut.dependencies:
            if dep.tag == key:
                print '   ', tag

    print 'The following concepts point to it:'
    for tag, node in db.nodes.items():
        for line in node.pointers:
            for item in line.items:
                if hasattr(item, 'link') and item.link == key:
                    print '   ', tag


def rank_bottleneck_scores():
    global db
    if db is None:
        load_db()

    graphs.rank_bottleneck_scores(db.nodes, db.graph)

def list_missing_dependencies():
    global db
    if db is None:
        load_db()

    nodes = database.read_nodes(config.CONTENT_PATH)
    for tag, node in nodes.items():
        for dep in node.dependencies:
            if dep.tag not in nodes:
                print tag, 'depends on', dep.tag


def find_resource(source):
    global db
    if db is None:
        load_db()

    items = []
    for tag in db.nodes:
        for r in db.nodes[tag].resources:
            if 'source' in r and r['source'] == source:
                items.append((tag, r))

    items.sort(key=lambda (tag, r): r['location'][0].text if 'location' in r else '')
    for tag, r in items:
        print tag
        print r
        print

def nodes_missing_summaries():
    global db
    if db is None:
        load_db()

    def missing_summary(node):
        return not node.summary or node.summary[:9] == 'Wikipedia'

    scores = graphs.page_rank(db.nodes)
    order = sorted(db.nodes.keys(), key=lambda t: scores[t], reverse=True)

    print 'With resources:'
    for key in order:
        node = db.nodes[key]
        if node.resources and missing_summary(node):
            print '   ', node.title
    print
    print 'No resources:'
    for key in order:
        node = db.nodes[key]
        if not node.resources and missing_summary(node):
            print '   ', node.title



##### checking the DB format #####

def errors_nonempty(errors):
    if type(errors) == str:
        return True
    elif type(errors) == list:
        for elt in errors:
            if errors_nonempty(elt):
                return True
        return False
    elif type(errors) == dict:
        for k, v in errors.items():
            if errors_nonempty(v):
                return True
        return False
    else:
        raise RuntimeError('Invalid type %s' % type(errors))

def print_errors(errors, indent=0):
    if type(errors) == str:
        print ' ' * indent + errors
    elif type(errors) == list:
        for e in errors:
            print_errors(e, indent=indent)
    elif type(errors) == dict:
        for k, v in errors.items():
            if errors_nonempty(v):
                print_errors(k, indent)
                print_errors(v, indent + 4)
    else:
        raise RuntimeError('Invalid type %s' % type(errors))


def check_db():
    global db
    if db is None:
        load_db()

    print_errors(database.check_all_node_formats(config.CONTENT_PATH))
    print_errors(db.check())


