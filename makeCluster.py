from hdbscan import HDBSCAN


def makeClusterDocs(embeddings, remaining_docs_with_keywords):
    print(f"\n>>> Clustering neglected Docs...")

    data_embeddings = embeddings.embed_documents([
        r[0].page_content 
        for r in remaining_docs_with_keywords])
    hdb = HDBSCAN(min_samples=1, min_cluster_size=3).fit(data_embeddings)
    remaining_docs_with_cat = filter(lambda x: x[1] != -1, zip([r[0].page_content for r in remaining_docs_with_keywords], hdb.labels_))

    cat_dict = {}

    for page_content, cat in remaining_docs_with_cat:
        if cat not in cat_dict:
            cat_dict[cat] = [page_content]
        else:
            cat_dict[cat].append(page_content)
            
    print(f">>> ...{len(cat_dict)} Clusters identified\n")
    
    return cat_dict
        