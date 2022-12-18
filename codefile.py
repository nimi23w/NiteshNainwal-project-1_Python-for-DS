# Importing pandas 
import pandas as pd
import numpy as np

# Importing fifa.csv dataset
data = pd.read_csv("fifa.csv")


# Checking first few samples
# 1st row
row1 = data.sample(n = 1)
print(row1)

# 0.1% data
rows_0_1 = data.sample(frac=0.1)
print(rows_0_1)


# Listing column headers for dataset
print(data.keys())

# Dropping columns not needed for data analysis
data = data[['ID', 'Name', 'Age', 'Nationality', 'Overall',
       'Potential', 'Club', 'Value', 'Wage', 'Preferred Foot',
       'International Reputation', 'Weak Foot', 'Skill Moves', 'Work Rate',
       'Body Type', 'Position', 'Jersey Number', 'Joined', 'Loaned From',
       'Contract Valid Until', 'Height', 'Weight', 'Crossing', 'Finishing',
       'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve',
       'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
       'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
       'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
       'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
       'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes', 'Release Clause']]
print(data.keys())


# Preprocessing 'Value' column
multi=[]
data['Value'] = data['Value'].str.slice(1)

for index in data.index:
    try:
        if data.loc[index,'Value'][-1]=="M":
            multi.append(float(1000000))        
        elif data.loc[index,'Value'][-1]=="K":
            multi.append(float(1000))
        else:
            multi.append(float(1))
    except:
        multi.append(float(0))

data['Mult']=multi
data['Value'] = data['Value'].str.slice(0,-1)
data['Value']=pd.to_numeric(data['Value'])
data['Value']=pd.to_numeric(data['Value']*data['Mult'])
data = data.drop('Mult', axis=1)

print(data['Value'].head(5))


# Similarly Preprocessing 'Wage' and 'Release Clause' columns
multiW=[]
multiR=[]
data['Wage'] = data['Wage'].str.slice(1)
data['Release Clause'] = data['Release Clause'].str.slice(1)

for index in data.index:
    try:
        if data.loc[index,'Wage'][-1]=="M":
            multiW.append(float(1000000))        
        elif data.loc[index,'Wage'][-1]=="K":
            multiW.append(float(1000))
        else:
            multiW.append(float(1))
    except:
        multiW.append(float(0))

for index in data.index:
    try:
        if data.loc[index,'Release Clause'][-1]=="M":
            multiR.append(float(1000000))        
        elif data.loc[index,'Release Clause'][-1]=="K":
            multiR.append(float(1000))
        else:
            multiR.append(float(1))
    except:
        multiR.append(float(0))
    

data['MultW']=multiW
data['Wage'] = data['Wage'].str.slice(0,-1)
data['Wage']=pd.to_numeric(data['Wage'])
data['Wage']=pd.to_numeric(data['Wage']*data['MultW'])

data['MultR']=multiR
data['Release Clause'] = data['Release Clause'].str.slice(0,-1)
data['Release Clause']=pd.to_numeric(data['Release Clause'])
data['Release Clause']=pd.to_numeric(data['Release Clause']*data['MultR'])

data = data.drop('MultR', axis=1)
data = data.drop('MultW', axis=1)

print(data[['Wage','Release Clause']].head(5))


# Preprocessing 'Joined' column                                                             #####
data['Joined'].bfill(inplace=True)
print(data["Joined"].astype(str).str[-4:].astype('int64'))

print(data['Joined'].head(5))


# Converting 'Contract Valid Until' to Pandas datetime format
data['Contract Valid Until']=pd.to_datetime(data['Contract Valid Until'])

print(data['Contract Valid Until'].head(5))


# Preprocessing 'Height' column
data['Height'] = data['Height'].str.split("'")
data['Height'] = (pd.to_numeric(data['Height'].str[0])*12)+(pd.to_numeric(data['Height'].str[1]))

print(data['Height'].head(5))


# Preprocessing 'Weight' column
data['Weight'] = pd.to_numeric(data['Weight'].str.split("lbs").str[0])

print(data['Weight'].head(5))


# Checking for % of missing values
#  By Rows
    # 'Joined' and 'Loaned From' columns are mutual so we will treat them as merged and subtract 1 from missing data count
    # to find if a row has missing data
data['Missing Data']=data.isnull().sum(axis=1)-1
count_missing_rows=len(data[data['Missing Data']>0])
per=(count_missing_rows*100)/len(data['Missing Data'])
print("% of Rows with missing entries in atleast one column: "+str(per)+" %")

# By Columns
missing_col=data.info()
print(missing_col)


# Imputing missing data
data['Club']=data['Club'].fillna(data['Club'].mode())
data['Value']=data['Value'].fillna(data['Value'].mean())
data['Wage']=data['Wage'].fillna(data['Wage'].mean())
data['Position']=data['Position'].fillna(data['Position'].mode())
data['International Reputation']=data['International Reputation'].fillna(data['International Reputation'].mean())
data['Jersey Number']=data['Jersey Number'].fillna(data['Jersey Number'].mean())
data['Release Clause']=data['Release Clause'].fillna(data['Release Clause'].mean())

print(data.info())


# Plotting Data
import matplotlib.pyplot as plt
data['Overall'].plot()
plt.show()

# Findings 
# The distribution of data using 'Overall' forms an almost smooth quadratic curve
# The curve tends towards 100 rating at lower players count and inflects to 0 rating as the player count increases
# The curve is available on 'Overall_Plot.png' file


# Retreiving name of top 20 players based on overall
print(data.sort_values('Overall',ascending = False).head(20)['Name'])

# Creating dataframe for top 20 players
top_20=data.sort_values('Overall',ascending = False).head(20)

# Average Age and Wage of top 20 players
top_20_age_wage=top_20[['Age','Wage']]
print("******************************************************")
print("Top 20 Players Stats")
print("Average Age: "+str(top_20_age_wage['Age'].mean()))
print("Average Wage: "+str(top_20_age_wage['Wage'].mean()))


# Highest Wage player
print("Highest Wage Player: ")
print(str(top_20.sort_values('Wage',ascending = False).head(1)[['Name','Wage']]))
print("******************************************************")


# Creating 'Club' based dataframe
data_club=data[['Name','Club','Wage','Overall']]
print(data_club)

# Average 'Overall' ratings based on 'Club'
data_club_avg=data_club[['Club','Wage','Overall']]
data_club_avg=data_club_avg.groupby('Club',as_index=False).mean()
print(data_club_avg[['Club','Overall']])

# Plotting 'Club' vs 'Overall' for top 10 clubs
data_club_avg_top10=data_club_avg.sort_values('Overall',ascending=False).head(10)[['Club','Overall']]
data_club_avg_top10.plot(x='Club',y='Overall',kind='bar')
plt.show()
# 'Club' vs 'Overall' can be seen from 'Club_based_overall_top10.png'


# Relationship between 'Age' and 'Potential'
data.plot.hexbin(x='Age',y='Potential')
plt.show()
# Plot can be seen at 'potential_vs_age.png'
# Findings:
# In the plot we can observe where greater proportions of players are located. There are more younger players with a potential around 
# the 75 mark while more ‘middle-aged’ players currently have a lower potential, around 70. Potential contnues to decrese to around
# 65 for 'old-aged' players.


# Factors effecting 'Wage'
data.plot.box(y=['Potential','Overall','Value','Age','International Reputation','Release Clause'],x='Wage')
plt.show()
# Plot can be seen at 'factors_effecting_wage.png'
# Findings:
# In the plot we can observe that the factors which effect player 'Wage' are 'Value' and 'Realease Clause'

# Player 'Position' plot
data_position=data.groupby('Position',as_index=False).size()
data_position=data_position.sort_values('size')
data_position.plot(y='size',x='Position',kind='bar')
plt.show()
# Plot can be seen at 'position_stats.png'
# Findings:
# Least played position: LF
# Most played position: ST


# Filtering players with Club='Juventus' and Wage>200K
data_filtered=data[(data['Club']=='Juventus') & (data['Wage']>200000)]
print(data_filtered)
# No. of such player = 3


# Filtering top 5 players for each position
positions=[]
positions=data_position['Position'].tolist()
top_5_by_position=data.head(0)

for index in positions:
    players_pos=data[(data['Position']==index)]
    players_pos=players_pos.sort_values('Overall',ascending=False).head(5)
    top_5_by_position=top_5_by_position.append(players_pos,ignore_index=True)
      
print(top_5_by_position)

# Average Wage of top 5 players for each position
positions_avg_wage=top_5_by_position[['Position','Wage']]
positions_avg_wage=positions_avg_wage.groupby('Position').mean()
print(positions_avg_wage)

data.to_csv("output_info.csv")