"""mkdocs-llmstxt preprocess hook: prepare rendered pages for their Markdown copies."""

DIRECTIVE = 'For AI agents: an index of this documentation is available at '


def preprocess(soup, output):
    """Point agents to /llms.txt and keep Mermaid source labelled; `output` is the Markdown path."""
    for pre in soup.select('pre.mermaid'):
        pre['class'] = pre['class'] + ['language-mermaid']
    paragraph = soup.new_tag('p')
    link = soup.new_tag('a', href='/llms.txt')
    link.string = 'llms.txt'
    paragraph.append(DIRECTIVE)
    paragraph.append(link)
    paragraph.append('.')
    soup.insert(0, paragraph)
