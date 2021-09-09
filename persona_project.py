import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.options.display.float_format = '{:.1f}'.format

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
data = pd.read_csv("datasets/persona.csv")

data.describe()
#          PRICE          AGE
# count  5000.000000  5000.000000
# mean     34.132000    23.581400
# std      12.464897     8.995908
# min       9.000000    15.000000
# 25%      29.000000    17.000000
# 50%      39.000000    21.000000
# 75%      39.000000    27.000000
# max      59.000000    66.000000

# ▪ Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
data['SOURCE'].value_counts()
# ▪ Soru 3: Kaç unique PRICE vardır?
data['PRICE'].nunique()
# ▪ Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()
# ▪ Soru 5: Hangi ülkeden kaçar tane satış olmuş?
data.groupby("COUNTRY").agg({'PRICE':'count'})
# ▪ Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
data.groupby("COUNTRY").agg({'PRICE':'sum'})
# ▪ Soru 7: SOURCE türlerine göre göre satış sayıları nedir?
data.groupby("SOURCE").agg({'PRICE':'count'})
# ▪ Soru 8: Ülkelere göre PRICE ortalamaları nedir?
data.groupby("COUNTRY").agg({'PRICE':'mean'})
# ▪ Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
data.groupby("SOURCE").agg({'PRICE':'mean'})
# ▪ Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir
data.groupby(["COUNTRY","SOURCE"]).agg({'PRICE':'mean'})

# Görev 2
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?

df = data.pivot_table(values=['PRICE'], columns=['COUNTRY', 'SOURCE', 'SEX', 'AGE'], aggfunc='mean')
df = df.unstack().unstack()

# Görev 3: Çıktıyı PRICE’a göre sıralayınız.
agg_df = df.sort_values(by=['PRICE'],ascending=False)

# Görev 4: Index’te yer alan isimleri değişken ismine çeviriniz

agg_df = agg_df.reset_index()

# Görev 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

# AGE değişken analizi ve görselleştirilmesi

series_x, bins = pd.cut(agg_df["AGE"],bins=5, retbins=True, labels=[0,1,2,3,4])
series_x.value_counts()

plt.scatter(agg_df.AGE,series_x)
plt.show()

sns.boxplot(x = series_x, y = agg_df['AGE'], palette = "ch:0.5")
plt.show()

agg_df["AGE"].min()
agg_df["AGE"].max()

bins = [14, 25, 35, 45, 55, 100]
group_names = ['15_25','26_35','36_45','46_55','55+']
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], bins, labels= group_names)

agg_df.head()

# Görev 6:
# Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

agg_df.dtypes


agg_df[['PRICE','AGE']] = agg_df[['PRICE','AGE']].astype(str) # floatve int, str'ye cevrildi

# örnek cıktı : BRA_ANDROID_MALE_41_66
[row for row in agg_df.values][0]
# array(['bra', 'android', 'male', '46', '59.0', '46_55']

agg_df.loc[:,"customers_level_based"] = [row[0].upper()+"_"+row[1].upper()+"_"+row[2].upper()+"_"+row[5] for row in agg_df.values]
agg_df.head()

# COUNTRY   SOURCE     SEX AGE PRICE AGE_CAT     customers_level_based
# 0     bra  android    male  46  59.0   46_55    BRA_ANDROID_MALE_46_55
# 1     usa  android    male  36  59.0   36_45    USA_ANDROID_MALE_36_45
# 2     fra  android  female  24  59.0   15_25  FRA_ANDROID_FEMALE_15_25
# 3     usa      ios    male  32  54.0   26_35        USA_IOS_MALE_26_35
# 4     deu  android  female  36  49.0   36_45  DEU_ANDROID_FEMALE_36_45

agg_df["PRICE"] = agg_df["PRICE"].astype(float)
agg_df[['customers_level_based','PRICE']].groupby("customers_level_based").agg({'PRICE':'mean'})
agg_df = agg_df[['customers_level_based','PRICE']].groupby("customers_level_based").agg({'PRICE':'mean'})
agg_df = agg_df.reset_index()
agg_df.loc[:,"SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df

# Segmentleri betimleyiniz:
agg_df.groupby("SEGMENT").agg({"PRICE":["mean","max","min","sum"]}).head()
#          mean  max  min   sum
# SEGMENT
# D        28.1 31.5 19.0 618.9
# C        33.0 34.0 31.6 726.8
# B        35.4 36.7 34.1 744.1
# A        39.7 49.0 36.7 873.6

# Görev 7: Yeni gelen müşterileri segmentlerine göre sınıflandırınız ve ne kadar gelir getirebileceğini tahmin ediniz.

# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

# agg_df tablosuna göre bu kişinin segmentini (grubunu) ifade ediniz.

new_user = "TUR_ANDROID_FEMALE_26_35"
#  customers_level_based    PRICE     SEGMENT
#  TUR_ANDROID_FEMALE_26_35   36.3       B

new_user = "FRA_IOS_FEMALE_26_35"
# customers_level_based  PRICE SEGMENT
# FRA_IOS_FEMALE_26_35   31.5       D

agg_df[agg_df["customers_level_based"] == new_user]

