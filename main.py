import mwparserfromhell
import xml.etree.ElementTree as ET



def filter_wiki_links_r(wiki: str) -> list[str]:
    links = mwparserfromhell.parse(wiki).filter_wikilinks()
    tmp = []
    for link in links:
        l = filter_wiki_links_r(link[2:-2]) # take [[x]] -> x
        if len(l) == 0:
            tmp.append(link)
            continue

        for ele in l:
            tmp.append(ele)


    result = []
    for item in tmp:
        s: str = item.split("|")[0]
        s = s.strip("[]")
        s = s.strip()
        s = f"[[{s}]]"

        if ":" not in s:
            result.append(s)

    return result

def strip_links(links: list[str]):
    return [l.strip("[]") for l in links]

def main() -> None:
    with open('graph.txt', 'a') as graph_file:
        root = ET.parse('small.xml').getroot()
        print("parsed")
        i = 0
        for child in root:
            article_title = child[0].text
            article_text = ""

            if ":" in article_title: # not a regular article, either a user: or a talk:
                continue

            i += 1
            if i % 1000 == 0:
                print(f"Parsed {i} articles")

            for a in child:
                if a.tag == '{http://www.mediawiki.org/xml/export-0.11/}revision':
                    for b in a:
                        if b.tag == '{http://www.mediawiki.org/xml/export-0.11/}text':
                            article_text = b.text

            links = filter_wiki_links_r(article_text)
            links = strip_links(links)

            graph_file.write(f"{article_title}:{links}\n")








if __name__ == "__main__":
    main()