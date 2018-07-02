import pandas as pd

if __name__ == '__main__':
    total_df = pd.DataFrame()
    with open('上海证券交易所上市公司列表.csv', encoding='utf8') as f:
        SH_df = pd.read_csv(f, keep_default_na=False, index_col=0)
        SH_df = SH_df.drop(SH_df.columns[[3, 6, 7]], axis=1)
        names = []
        codes = []
        for i in range(len(SH_df['公司全称'])):
            name = SH_df.loc[i, 'A股简称'] if len(SH_df.loc[i, 'A股简称']) != 0 else SH_df.loc[i, 'B股简称']
            code = SH_df.loc[i, 'A股代码'] if len(SH_df.loc[i, 'A股代码']) != 0 else SH_df.loc[i, 'B股代码']
            names.append(name)
            codes.append(code)
        SH_df.insert(0, '公司简称', names)
        SH_df.insert(0, '公司代码', codes)
        df = SH_df.drop(SH_df.columns[[3, 4, 5, 6]], axis=1)
        total_df = total_df.append(df, ignore_index=True)
    with open('深圳证券交易所上市公司列表.csv', encoding='utf8') as f:
        SZ_df = pd.read_csv(f, keep_default_na=False, index_col=0, dtype=str)
        SZ_df = SZ_df.drop(SZ_df.columns[[3, 4, 5, 6, 7, 8, 9]], axis=1)
        total_df = total_df.append(SZ_df, ignore_index=True)
    with open('深圳证券交易所中小板上市公司列表.csv', encoding='utf8') as f:
        df = pd.read_csv(f, keep_default_na=False, index_col=0, dtype=str)
        df = df.drop(df.columns[[3, 4, 5, 6]], axis=1)
        total_df = total_df.append(df, ignore_index=True)
    with open('深圳证券交易所创业板上市公司列表.csv', encoding='utf8') as f:
        df = pd.read_csv(f, keep_default_na=False, index_col=0, dtype=str)
        df = df.drop(df.columns[[3, 4, 5, 6]], axis=1)
        total_df = total_df.append(df, ignore_index=True)
    total_df.to_csv('company.csv', sep=',')
