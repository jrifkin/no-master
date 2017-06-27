
# coding: utf-8

# In[2]:

#imports and setup
import pandas as pd
import numpy as np
import sqlite3


# In[3]:

# 1 Import CSVs into data frames

# Read the 3 CSV files pulled from SSCC. Note that df_customer CSV has an extra column 
# end of file that provides no useful information and is omitted from the read with
# the usecols statement
df_customer = pd.read_csv("data/jrq156_pilot_customer.csv",header=0                          ,usecols=range(0,450))
df_item = pd.read_csv("data/jrq156_pilot_item.csv",header=0)
df_mail = pd.read_csv("data/jrq156_pilot_mail.csv",header=0)

# print list of df_mail columns and first 5 records of mail
print df_mail.columns
print df_mail.head()


# In[4]:

# 2 verify that there are no duplicates in customer data
for col in df_customer.columns.tolist():
    # value_counts performs a groupby with a simple count on each column
    # The max number in the column shows the max count of that key per column
    # columns with a max count = 1 are unique customer identifier columns
    # and should be omitted when checking for duplicates
    if df_customer[col].value_counts().max() == 1:
        print "Unique Column: %s"%(col)

# Use duplicated to count num of duplicated customers ommitting the unique columns 
num_dupes = sum(df_customer.ix[:,[i for i,x in enumerate(df_customer.columns)                                  if x!= 'acctno']].duplicated())
print "Customer table has %d duplicates"%(num_dupes)


# In[7]:

# 3 Check the item and mail data to determine whether there are any 
# records in them for customers who are not in the customer data.

# To check the item and mail table for records that are not contained in the
# customer table the mail and item tables are outer joined with the indicator 
# option as true. indicator=True specifies which table the record comes from 
# which can be both, left_only, or right_only. Mail and Item are the right 
# tables in the two join operations so any records that have right_only are 
# only contained in either mail or item. These would be records of customers 
# in the mail and item tables that are not included in the customer table.
df_customer_mail = pd.merge(df_customer, df_mail,how='outer',on='acctno'                            ,indicator=True)
df_customer_item = pd.merge(df_customer,df_item,how='outer',on='acctno'                            ,indicator=True)

# count number of right, left, and both keys
mail_check =  df_customer_mail._merge.value_counts()
item_check = df_customer_item._merge.value_counts()

print "Mail contains %d unmatched customer accounts."%(mail_check.loc['right_only'][0])
print "Item contains %d unmatched customer accounts."%(item_check.loc['right_only'][0])


# In[8]:

# 4 db load

# create connection to xyz.db
con = sqlite3.connect("xyz.db")

# populate the db with customer, item, and mail data
df_customer.to_sql("customer",con,flavor='sqlite',if_exists='replace',index=False)
df_item.to_sql('item',con,flavor='sqlite',if_exists='replace',index=False)
df_mail.to_sql('mail',con,flavor='sqlite',if_exists='replace',index=False)

#confirm data exists by querying the data
# create a sql cursor to query
cur = con.cursor()

# write a simple query
query = 'select * from customer limit 2'

# execute the simple query
result = cur.execute(query)

# print first 10 columns of first row of the results
print result.fetchall()[0][0:10]


# In[9]:

# 5 

# define a naive encoder to apply to columns
def encoder(x):
    """Encoder takes in a value, compares
    the value to 'Y' and assigns a 1 for
    true and 0 for false."""
    val = 0
    if x == 'Y':
        val = 1
    return val

#clean duplicates out of mail table 
df_mail_deduped = df_mail.drop_duplicates()
df_mail_deduped.duplicated()

#count number of times an account is mailed
df_mail_deduped['tot_mail_sent'] = df_mail_deduped.sum(axis=1)

#filter to 5 or more mailings
df_mail_5 = df_mail_deduped[df_mail_deduped.tot_mail_sent>=5]

#merge the 5 or more mailing dataframe with the customers
df_mail5_merge = pd.merge(df_mail_5,df_customer,on='acctno',how='inner',indicator=True)

# define the columns to keep
keep_cols = ['acctno','tot_mail_sent','ytd_transactions_2009',
             'ytd_sales_2009','zhomeent','zmobav']

#filter to specified columns
df_mail5_merge = df_mail5_merge[keep_cols]

#make encoded columns
for col in keep_cols:
    # naive column identifier
    if col[0] == 'z':
        # apply the encoder to the column
        df_mail5_merge[col + '01'] = df_mail5_merge[col].apply(encoder)

# final data to CSV file
df_mail5_merge.to_csv('xyz-marketing-campaign.csv',header=True,index=False)


# In[10]:

# fill NaNs so that they appear in the crosstabulation
df_cross = df_mail5_merge.fillna('NaN')

# create a cross tab to verify encoding works
print "Total customers that have been mailed 5 or more times: %d"%(len(df_mail5_merge))

pd.crosstab(df_cross.zhomeent,df_cross.zhomeent01)

# 11392 = 897 + 8586 + 1909. Passes check and no confused vals


# In[11]:

# second crosstab of zmobav
pd.crosstab(df_cross.zmobav,df_cross.zmobav01)

# 11392 = 897 + 10166 + 329. Passes check and no confused vals


# In[12]:

#pickle the data frames

#make a dictionary of dataframes
d_df = {'df_cross':df_cross
        ,'df_customer':df_customer
        ,'df_customer_item':df_customer_item
        ,'df_customer_mail':df_customer_mail
        ,'df_item':df_item
        ,'df_mail':df_mail
        ,'df_mail5_merge':df_mail5_merge
        ,'df_mail_5':df_mail_5
        ,'df_mail_deduped':df_mail_deduped}

for name,frame in d_df.iteritems():
    frame.to_pickle(name + ".pkl")

# commit the db write
con.commit()
# close the db connection
con.close()

