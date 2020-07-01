import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn import linear_model
df=pd.read_csv("cneos_closeapproach_data (2).csv")
df.dropna(inplace=True)
print(df.count())
print(df.info())
d=df["Object"].value_counts()
df[["min_distance","min_d"]]=df["CA Distance Minimum (LD | au)"].str.split("|",expand=True)
df[["Date","notnessary","n1"]]=df["Close-Approach (CA) Date"].str.split(" ",expand=True)
df.drop(["notnessary","n1"],axis=1)
df["min_distance_LD"] = df["min_distance"].apply(pd.to_numeric, downcast='float', errors='coerce')
df["min_d"] = df["min_d"].apply(pd.to_numeric, downcast='float', errors='coerce')
df[["year","mon","date"]]=df["Date"].str.split("-",expand=True)
df[["Min_Estimated_Diameter","Max_Estimated_diameter"]]=df["Estimated Diameter"].str.split("-",expand=True)
df[["Max_Estimated_diameter_m","m/km"]]=df["Max_Estimated_diameter"].str.split("m",expand=True)
df[["Max_Estimated_diameter_km","km"]]=df["Max_Estimated_diameter"].str.split("k",expand=True)
df[["Max_Estimated_diameter_m"]] = df["Max_Estimated_diameter_m"].apply(pd.to_numeric, downcast='float', errors='coerce')
df[["Max_Estimated_diameter_km"]] = df["Max_Estimated_diameter_km"].apply(pd.to_numeric, downcast='float', errors='coerce')
df["year"] = df["year"].apply(pd.to_numeric, downcast='float', errors='coerce')
a=df["Object"].value_counts().index.tolist()[:11]
b=df["Object"].value_counts().tolist()[:11]
c=[]
# top 10 most visited asteroids
for i in a:
  M1=df.loc[df['Object'] == i ]
  m1=M1["Estimated Diameter"].values.tolist()[:1]
  c.append(m1)
df_top_ten=pd.DataFrame({"Asteroid":a,"no.of visits":b,"Estimated_diameter":c})
print("TOP TEN THE MOST VISITED NEAR EARTH OBJECTS")
print(df_top_ten)
#top_ten_the_largest_Asteroids
diameter_in_meters=df[(df.Max_Estimated_diameter_m>500)]
diameter_in_meters=diameter_in_meters.sort_values(by='Max_Estimated_diameter_m', ascending=False)
l_in_m=diameter_in_meters["Object"].values.tolist()
diameter_in_km=df[(df.Max_Estimated_diameter_km>1)]
diameter_in_km=diameter_in_km.sort_values(by='Max_Estimated_diameter_km', ascending=False)
print(diameter_in_km["Max_Estimated_diameter_km"])
the_largest=diameter_in_km["Object"].value_counts().index.tolist()
the_largest_NEO_unique_values=diameter_in_km["Object"].unique().tolist()
the_largest.append(l_in_m)
t_l=the_largest[:11]
tl=the_largest_NEO_unique_values[:11]
l=[]
d1=[]
G=[]
for j in tl:
  A1=df.loc[df['Object'] == j ]
  m1=A1["Estimated Diameter"].values.tolist()[:1]
  l1=A1["Date"].values.tolist()[-1]
  G1=A1["CA Distance Minimum (LD | au)"].values.tolist()[-1]
  l.append(m1)
  d1.append(l1)
  G.append(G1)
df_the_largest=pd.DataFrame({"Asteroid":tl,"Estimated_diameter":l,"Close Approach Date in near future":d1,"Min_Distance(LD|au)":G})
print("TOP TEN THE LARGEST KNOWN NEAR EARTH OBJECTS ")
print(df_the_largest)
# The closest NEO'S
hit=df[(df.min_distance_LD<0.5) & (df.Max_Estimated_diameter_m>500)]
hit_larger_diameter_in_km=df[(df.min_distance_LD<0.5) &  (df.Max_Estimated_diameter_km>=1)]
hit=hit.sort_values(by='min_distance_LD', ascending=False)
hit_larger_diameter_in_km=hit_larger_diameter_in_km.sort_values(by='min_distance', ascending=False)
hit=hit.drop(['CA Distance Nominal (LD | au)','H (mag)','notnessary','min_distance','Unnamed: 8', 'min_d','Close-Approach (CA) Date','V relative (km/s)','CA Distance Minimum (LD | au)','V infinity (km/s)', 'n1', 'year', 'mon','date', 'Max_Estimated_diameter','Max_Estimated_diameter_m', 'm/km', 'Max_Estimated_diameter_km', 'km','Min_Estimated_Diameter'],axis=1)
hit_larger_diameter_in_km=hit_larger_diameter_in_km.drop(['CA Distance Nominal (LD | au)','min_distance','H (mag)','notnessary','Unnamed: 8','Close-Approach (CA) Date','V relative (km/s)','CA Distance Minimum (LD | au)','V infinity (km/s)', 'min_d', 'n1', 'year', 'mon','date', 'Max_Estimated_diameter','Max_Estimated_diameter_m', 'm/km', 'Max_Estimated_diameter_km', 'km','Min_Estimated_Diameter'],axis=1)
print(hit.columns)
pd.set_option('display.max_columns', None)
print("Close approach less than 0.5 LD and diameter in the range(500m-1km)")
print(hit)
print("Close approach less than 0.5 LD and diameter in the range(1km - and so on) ")
print(hit_larger_diameter_in_km)

# I predicted for only one asteroid, you can use the for loop as above to predict the values of other Asteroids
Most_visted_one=df.loc[df['Object'] == "(2019 BE5)" ]
Most_visted_one=Most_visted_one[(Most_visted_one.min_distance_LD<5)]
a=np.mean(Most_visted_one["V relative (km/s)"].values)
X=Most_visted_one[["year", "V relative (km/s)", "H (mag)" ]]
Y=Most_visted_one["min_distance_LD"].values
x_train,x_test,y_train,y_test = sklearn.model_selection.train_test_split(X,Y,test_size=0.33,random_state=0)
lm=linear_model.LinearRegression()
lm.fit(x_train,y_train)
y_predict=lm.predict(x_test)
prediction=[]
years=[]
for i in range(2200,2600):
    p=y_predictnew=lm.predict([[i,a,25.1]])
    prediction.append(p)
for j in range(2200,2600):
    years.append(j)
sns.set(style="ticks", context="talk")
plt.style.use("dark_background")
ax = sns.scatterplot(years,prediction,data=Most_visted_one)
plt.setp(ax.get_xticklabels(), rotation=90)
plt.xlabel("years")
plt.ylabel("Close-Approach in LD")
plt.title("NEO:(2019 BE5)")
plt.show()
print("NEO:(2019 BE5)")
print("Analysed:likely to enter earth's atmosphere in 2433")
p = y_predictnew = lm.predict([[2433, a, 25.1]])
print(p)

