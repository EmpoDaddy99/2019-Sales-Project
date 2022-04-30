import pandas as pd
import matplotlib.pyplot as plt

#Read Data
data = [pd.read_csv('Sales_January_2019.csv'), pd.read_csv('Sales_February_2019.csv'),
        pd.read_csv('Sales_March_2019.csv'), pd.read_csv('Sales_April_2019.csv'), pd.read_csv('Sales_May_2019.csv'),
        pd.read_csv('Sales_June_2019.csv'), pd.read_csv('Sales_July_2019.csv'), pd.read_csv('Sales_August_2019.csv'),
        pd.read_csv('Sales_September_2019.csv'), pd.read_csv('Sales_October_2019.csv'),
        pd.read_csv('Sales_November_2019.csv'), pd.read_csv('Sales_December_2019.csv')]

total_data = pd.concat([i for i in data[0:]], axis=0, ignore_index=True)
total_data = total_data[total_data.Product != 'Product']
total_data.to_csv('Total_Sales_2019.csv')

#Organize Data
for i in range(len(data)):
    data[i] = data[i].dropna()
    data[i] = data[i].reset_index()
    data[i]['Quantity Ordered'] = pd.to_numeric(data[i]['Quantity Ordered'], errors='coerce')
    data[i]['Price Each'] = pd.to_numeric(data[i]['Price Each'], errors='coerce')
    data[i].replace(" ", 'Nan', inplace=True)
    data[i] = data[i].drop(columns=['index'])
total_data = total_data.dropna()
total_data = total_data.reset_index()
total_data['Quantity Ordered'] = pd.to_numeric(total_data['Quantity Ordered'], errors='coerce')
total_data['Price Each'] = pd.to_numeric(total_data['Price Each'], errors='coerce')
total_data.replace(" ", float("NaN"), inplace=True)
total_data = total_data.drop(columns=['index'])

#Sales Outcomes
print('Sales Outcomes:')
monthly_rev = [None]
for i in range(len(data)):
    data[i]['Revenue'] = data[i]['Quantity Ordered'] * data[i]['Price Each']
    print("Month", str(i+1), "\n", data[i]['Revenue'].sum())
    monthly_rev.append(data[i]['Revenue'].sum())
print('Total Sales Outcomes:')
total_data['Revenue'] = total_data['Quantity Ordered'] * total_data['Price Each']
print(total_data['Revenue'].sum())
plt.plot(monthly_rev)
plt.axis([0,13,0,5000000])
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.show()
print()

#City with most product sales
print('City with most product sales per month:')
for i in range(len(data)):
    print('Month', str(i + 1) + ':')
    data[i]['City'] = pd.Series(data[i]['Purchase Address'].str.split(','))
    data[i]['City'] = data[i]['City'].str[1]
    result = data[i].groupby(['City']).sum()['Revenue'].sort_values(ascending = False)
    print(result)
print('City with most total product sales:')
total_data['City'] = pd.Series(total_data['Purchase Address'].str.split(','))
total_data['City'] = total_data['City'].str[1]
result = total_data.groupby(['City']).sum()['Revenue'].sort_values(ascending = False)
print(result)
plt.clf()
total_data.groupby(['City']).sum()['Quantity Ordered'].plot(x = 'City', y = 'Quantity Ordered', kind = 'bar')
plt.show()

#Average time bought
total_data['Order Time'] = pd.Series(total_data['Order Date'].str.split(' '))
total_data['Order Time'] = total_data['Order Time'].str[1]
plt.clf()
total_data.groupby(['Order Time']).sum()['Revenue'].plot(x = 'Order Time', y = 'Revenue', kind = 'line')
plt.show()

#Products sold together
print('Products sold together')
total_data.groupby(['Order Date', 'Purchase Address']).filter(lambda x: x['Product'].count() >= 4).to_csv('Total_Sales_Common_Items_2019')
l = pd.read_csv('Total_Sales_Common_Items_2019')
l = l.drop(columns=['Revenue', 'City', 'Order Time'])
l.to_csv('Total_Sales_Common_Items_2019')
print(l.groupby(['Product']).sum()['Quantity Ordered'].sort_values(ascending=False).head(10))

#Products most sold
print('Products most sold')
print(total_data.groupby(['Product']).sum()['Quantity Ordered'].sort_values(ascending=False).head(10))