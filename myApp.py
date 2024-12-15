import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title = 'python first app',
    page_icon = '👸'
)

#title
st.title(':rainbow[python first ap]',)
st.subheader(':gray[Explore data from app]',divider='rainbow')

file =st.file_uploader('Drop file',type=['csv','xlsx'])
print(file)
if(file != None):
    if(file.name.endswith('csv')):
        data =pd.read_csv(file)
    else:
        data =pd.read_excel(file)
    
    st.dataframe(data)
    st.info('File uploaded successfully',icon='✌️')

    st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and Bottom Row','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in the dataset and {data.shape[1]} columns in the dataset')
        st.subheader(f':gray[Statistical Summary  of the dataset at {data.shape[0]} rows]')
        st.dataframe(data.describe())

    with tab2:
        # st.write(f'There are {data.shape[0]} rows in the dataset and {data.shape[1]} columns in the dataset')
        st.subheader(f':gray[Statistical Top 3 rows of the dataset]')
        topRows = st.slider('Number of row you want to display',1,data.shape[0],key='topslider')
        st.dataframe(data.head(topRows))

        st.subheader(f':gray[Statistical Bottom 3 rows of the dataset]')
        bottomRows = st.slider('Number of row you want to display',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomRows))

    with tab3:
        st.subheader(f':gray[data type of the dataset columns]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader(f':gray[column name in the dataset]')
        st.write(list(data.columns))

    st.subheader(f':rainbow[Column value to count]',divider='rainbow')
    with st.expander('Value Count') :
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows',min_value =1,step=1)

        count = st.button( 'count')
        if(count ==True):
            result = data[column].value_counts().reset_index().head()
            
            st.dataframe(result)
            st.subheader('visualization',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',template='plotly_white')
            st.plotly_chart(fig)
            fig =px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.write('The group by your summarize data')
    st.subheader(':rainbow[Group by simplify data analysis]',divider='gray')
    with st.expander('Group by column'):
        col1,col2,col3 = st.columns(3)

        with col1:
            groupby_col = st.multiselect('Choose a group by column',options=list(data.columns))

        with col2:
            operation_col = st.selectbox('Choose operation column',options=list(data.columns))

        with col3:
            operation =st.selectbox('Choose operation to perform',options=['SUM','MAX','MIN','MEDIAN','COUNT'])

        if(groupby_col):
            result = data.groupby(groupby_col).agg(
            newcol = (operation_col,operation.lower())
            ).reset_index()
            st.dataframe(result)

            # st.subheader('visualization',divider='gray')
            # fig = px.bar(data_frame=result,x=groupby_col,y='newcol',text='newcol',template='plotly_white')
            # st.plotly_chart(fig)
            # fig = px.line(data_frame=result,x=groupby_col,y='newcol',template='plotly_white')
            # st.plotly_chart(fig)


            st.subheader(':rainbow[ Data visualization]',divider=True)
            graph = st.selectbox('Select graph',options=['line','bar','scatter','pie','sunburst'])
            if(graph == 'line'):
                x_axis = st.selectbox('Select column on x axis',options=list(result.columns))
                y_axis = st.selectbox('Select column on y axis',options=list(result.columns))
                color = st.selectbox('Select color',options=[None] + list(result.columns))
                fig =px.line(data_frame=result,x=x_axis,y=y_axis,color=color)
                st.plotly_chart(fig)

            elif(graph == 'bar'):
                x_axis = st.selectbox('Select column on x axis',options=list(result.columns))
                y_axis = st.selectbox('Select column on y axis',options=list(result.columns))
                color = st.selectbox('Select color',options=[None] + list(result.columns))
                facet_column =st.selectbox('Select text column',options=[None] + list(result.columns))
                fig =px.bar(data_frame=result,x=x_axis,y=y_axis,facet_col=facet_column,color=color,barmode='group')
                st.plotly_chart(fig)

            elif(graph == 'scatter'):
                x_axis = st.selectbox('Select column on x axis',options=list(result.columns))
                y_axis = st.selectbox('Select column on y axis',options=list(result.columns))
                color = st.selectbox('Select color',options=[None] + list(result.columns))
                size =st.selectbox('Select column',options=[None] + list(result.columns))
                fig =px.scatter(data_frame=result,x=x_axis,y=y_axis,size=size,color=color)
                st.plotly_chart(fig) 

            elif(graph == 'pie'):
                name = st.selectbox('Select column name',options=list(result.columns))
                values = st.selectbox('Select column values',options=list(result.columns))
                color = st.selectbox('Select color',options=[None] + list(result.columns))
                # size =st.selectbox('Select column',options=[None] + list(result.columns))
                fig =px.pie(data_frame=result,names=name,values=values,color=color)
                st.plotly_chart(fig) 

            elif(graph == 'sunburst'):
                name = st.multiselect('Select column name',options=list(result.columns))
                values = st.selectbox('Select column values',options=list(result.columns))
                color = st.selectbox('Select color',options=[None] + list(result.columns))
                # size =st.selectbox('Select column',options=[None] + list(result.columns))
                fig =px.sunburst(data_frame=result,path=name,values=values,color=color)
                st.plotly_chart(fig) 
