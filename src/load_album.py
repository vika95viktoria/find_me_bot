import pickle

def process_album(album_name: str):
    load_album(album_name)
    all_ambeddings_list = []
    index_to_image_map = {}
    index = 0
    for photo in album:
        embs = get_ambeddings(photo)
        for _ in embs:
            index_to_image_map[index] = photo.name
            index += 1
        all_ambeddings_list.extend(embs)
    [emb for ph in album for emb in get_embeddings(photo)]
    index = FaissIndex(all_ambeddings_list)
    with open('new_index.pkl', 'wb') as file:
        pickle.dump(index, file)

    gcp_service.upload_to_bucket('new_index.pkl')
