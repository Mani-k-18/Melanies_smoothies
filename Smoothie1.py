# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

#noe section to display smoothiefroot nutrition

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response)
sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width = true)


#Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie :cup_with_straw: ")
st.write(
  """choose the fruit you want in your custom smoothie """
)



 
name_on_order = st.text_input('Name on smoothie')
st.write('The name on your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))

Ingredient_list = st.multiselect(
    "Choose upto 5 ingredients: ",
    my_dataframe,
    max_selections= 5
)

if Ingredient_list:
   #st.write(Ingredient_list)
   #st.text(Ingredient_list)

   Ingredient_string = ''

   for fruit_chosen in Ingredient_list:
       Ingredient_string += fruit_chosen + ' '

      # search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

   #st.write(Ingredient_string)

   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + Ingredient_string + """','""" + name_on_order + """')"""

       #st.write(my_insert_stmt)
   time_to_insert = st.button('Submit order')

   if time_to_insert:
       session.sql(my_insert_stmt).collect()

  
       
       st.success('Your Smoothie is ordered!', icon="✅")
       #st.stop
