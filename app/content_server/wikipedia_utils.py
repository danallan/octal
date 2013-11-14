import os
import urllib, urllib2
from xml.dom.minidom import parse as parseXML
import config
import formats

def write_wiki_summary(node_title, node_dir):
    """
    Obtain 1 sentence summaries from wikipedia for corresponding wikipedia page for 'node_title'
    node_title: title to be used for wikipedia query
    node_dir: directory containing content for given node (wiki_summary_file will be written here)
    wiki_summary_file: directory containing the node directories
    """
    # try to obtain a wiki summary
    wiki_ep = 'http://en.wikipedia.org/w/api.php'
    urlparams = '?action=query&redirects&prop=extracts&exintro&explaintext&exsectionformat=plain&exsentences=1&format=xml&titles=%s'\
                %  urllib.quote_plus(node_title)
    rquest = urllib2.Request(wiki_ep + urlparams)
    xmlresp = parseXML(urllib2.urlopen(rquest))
    extxt = xmlresp.getElementsByTagName('extract')
    if len(extxt):
        summary = extxt[0].firstChild.wholeText.replace('\n',' ')
    else:
        summary = ''
    # cache the wiki summary
    temp, tag = os.path.split(node_dir)
    content_path, _ = os.path.split(temp)
    wiki_summary_file = formats.wiki_summary_file(content_path, tag)
    with open(wiki_summary_file, 'w') as wikif:
        wikif.write(summary.encode('utf-8'))

if __name__=="__main__":
    nodes = formats.read_nodes(config.CONTENT_PATH)
    for node_tag in nodes:
        node = nodes[node_tag]
        node_dir = os.path.join(config.CONTENT_PATH, 'nodes', node.tag)
        summary_file = formats.summary_file(config.CONTENT_PATH, node.tag)
        wiki_summary_file = formats.wiki_summary_file(config.CONTENT_PATH, node.tag)
        
        if not os.path.exists(summary_file) and not os.path.exists(wiki_summary_file):
            if node.title:
                ttl = node.title
            else:
                ttl = node.tag
            write_wiki_summary(ttl, node_dir)
