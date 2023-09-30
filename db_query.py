import chromadb
import config


def get_chroma_response(query):
    """
    Get a response from the Chroma database
    :param query: The query to send to the database
    :return: A response from the database
    """

    chroma_client = chromadb.PersistentClient(path=config.DB_LOCATION)

    collection = chroma_client.get_collection(name=config.DB_NAME)

    results = collection.query(
        query_texts=[query],
        n_results=30
    )

    return results


if __name__ == "__main__":
    print("For use as an import")
