"""Loader and executor of finscrap module."""

if __name__ == "__main__":
    from finscrap import finscrap

    print("LOADING")

    analizy = finscrap.GetAssetAnalizy("analizy.pl")
    analizy.get_data()

    biznesr = finscrap.GetAssetBiznesR("biznesradar.pl")
    biznesr.get_data()

    borsa = finscrap.GetAssetBorsa("borsa")
    borsa.get_data()

    ishares = finscrap.GetAssetIShares("ishares")
    ishares.get_data()
