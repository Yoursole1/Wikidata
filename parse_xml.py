import mwparserfromhell
import xml.etree.ElementTree as ET
import glob



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
            result.append(s) # todo look into improving this

    return result

def strip_links(links: list[str]):
    return [l.strip("[]") for l in links]

def main() -> None:
    i = 0
    xml_files = glob.glob("*.xml")
    with open('graph.txt', 'a') as graph_file:
        for xml in xml_files:
            root = ET.parse(xml).getroot()
            print("Initial Parse Done: " + xml)
            for child in root:
                article_title = child[0].text
                article_text = ""

                i += 1
                if i % 1000 == 0:
                    print(f"Parsed {i} articles")

                skip = False

                for a in child:
                    if a.tag == '{http://www.mediawiki.org/xml/export-0.11/}revision':
                        for b in a:
                            if b.tag == '{http://www.mediawiki.org/xml/export-0.11/}text':
                                article_text = b.text
                    elif a.tag == '{http://www.mediawiki.org/xml/export-0.11/}ns' and a.text != '0':
                        skip = True

                    elif a.tag == '{http://www.mediawiki.org/xml/export-0.11/}redirect':
                        skip = True


                if skip:
                    continue

                print(article_title)

                links = filter_wiki_links_r(article_text)
                links = strip_links(links)
                links = list(set(links)) # remove duplicates

                graph_file.write(f"{article_title}:{links}\n")








if __name__ == "__main__":
    main()