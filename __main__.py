if __name__ == "__main__":
    import webscrap
    print("LOADING")

    analizy = webscrap.GetAssetAnalizy("analizy.pl")
    analizy.get_data()

    biznesr = webscrap.GetAssetBiznesR("biznesradar.pl")
    biznesr.get_data()

    borsa = webscrap.GetAssetBorsa("borsa")
    borsa.get_data()

    ishares = webscrap.GetAssetIShares("ishares")
    ishares.get_data()
