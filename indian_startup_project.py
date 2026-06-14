import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout='wide', page_title='Startup Analysis')

df = pd.read_csv('cleaned_startup_data.csv')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month_name()


def load_investor_details(investor):
    st.title(investor.title())
    # load the recent 5 investments
    recent_investments = df[df['investors'].str.contains(investor)].head()[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(recent_investments)
    col1, col2 = st.columns(2)

    with col1:
        # load 5 biggest investments
        top_investments = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('Top 5 Investments')
        fig, ax = plt.subplots()
        ax.bar(top_investments.index, top_investments.values)
        st.pyplot(fig)

    with col2:
        # load common investment sectors
        st.subheader('Common Investment Sectors')
        sector = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(sector, labels=sector.index, autopct='%0.1f%%')
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        # load common round in which investors usually invest
        st.subheader('Common Rounds Of Investments')
        rounds = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(rounds, labels=rounds.index, autopct='%0.1f%%')
        st.pyplot(fig)

    with col4:
        # load common cities where investors usually invest
        st.subheader('Common Cities Of Investments')
        city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(
            ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(city, labels=city.index, autopct='%0.1f%%')
        st.pyplot(fig)

    # line chart of how investment has changed with years
    st.header('year-wise investment status')
    yearly_investment = df[df['investors'].str.contains(investor)].groupby(df['date'].dt.year)['amount'].sum()
    fig1, ax1 = plt.subplots()
    ax1.plot(yearly_investment.index, yearly_investment.values)
    st.pyplot(fig1)


def load_general_analysis():
    st.title('Overall Analysis')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # total invested amount
        total_investment = round(df['amount'].sum())
        st.metric('Total', str(total_investment) + ' CR')
    with col2:
        # maximum invested amount
        max_investment = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum', str(max_investment) + ' CR')
    with col3:
        # average invested amount
        avg_investment = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average', str(avg_investment) + ' CR')
    with col4:
        # total number of startup
        total_count = df['startup'].nunique()
        st.metric('Total Startups', total_count)

    opt1 = st.selectbox('Analyze Based On', ['year', 'month'])

    if opt1 == 'year':
        opt2 = st.selectbox('Analyze Based On', ['no.of startups funded', 'amount of money invested'])
        if opt2 == 'no.of startups funded':
            # yearly analysis of no of startups funded
            temp_df = df.groupby('year')['startup'].count()
            fig, ax = plt.subplots()
            ax.plot(temp_df.index, temp_df.values)
            st.pyplot(fig)
        elif opt2 == 'amount of money invested':
            # yearly analysis of amount of money invested
            temp_df = df.groupby('year')['amount'].sum()
            fig, ax = plt.subplots()
            ax.plot(temp_df.index, temp_df.values)
            st.pyplot(fig)
    elif opt1 == 'month':
        opt3 = st.selectbox('select the year', df['year'].unique().tolist())
        opt2 = st.selectbox('Analyze Based On', ['no.of startups funded', 'amount of money invested'])
        temp_df1 = df[df['year'] == opt3]
        if opt2 == 'no.of startups funded':
            # month by month analysis of a particular year based on no.of startups funded
            temp_df = temp_df1.groupby('month')['startup'].count()
            fig, ax = plt.subplots()
            ax.plot(temp_df.index, temp_df.values)
            st.pyplot(fig)
        elif opt2 == 'amount of money invested':
            # month by month analysis of a particular year based on the amount of money invested
            temp_df = temp_df1.groupby('month')['amount'].sum()
            fig, ax = plt.subplots()
            ax.plot(temp_df.index, temp_df.values)
            st.pyplot(fig)

    st.header('Top Sectors')
    col5, col6 = st.columns(2)

    with col5:
        # analysis of top sectors in terms of no of startups being funded
        st.subheader('based on no.of startups funded')
        temp_df = df.groupby('vertical')['startup'].count().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(temp_df.values, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig)
    with col6:
        # analysis based on top sectors based on amount money invested in a particular sector
        st.subheader('based on amount of money invested')
        temp_df = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(temp_df.values, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig)

    col7, col8 = st.columns(2)

    with col7:
        # load top investors who have invested largest amount of money
        st.subheader('Top Investors')
        temp_df = df.groupby('investors')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(temp_df.values, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig)
    with col8:
        # Top cities which have received highest amount of funds
        st.subheader('Top Cities')
        temp_df = df.groupby('city')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(temp_df.values, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig)

    st.header('Top Startups')
    opt4 = st.selectbox('Select One', ['year-wise', 'Overall'])
    if opt4 == 'year-wise':
        # year wise top startups which received highest amounts of funding that year
        opt5 = st.selectbox('Select the year',df['year'].unique().tolist())
        temp_df = df[df['year'] == opt5]
        temp_df1 = temp_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(temp_df1.index,temp_df1.values)
        st.pyplot(fig)
    elif opt4 == 'Overall':
        # overall top startups
        temp_df = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.pie(temp_df.values, labels=temp_df.index, autopct='%0.1f%%')
        st.pyplot(fig)


def load_startup_analysis(startup):
    st.title(startup)
    col1, col2, col3 = st.columns(3)
    temp_df = df[df['startup'] == startup].head(1)
    with col1:
        verticals = df[df['startup'] == startup]['vertical'].unique().tolist()
        st.metric('Industry', ', '.join(map(str, verticals)))
    with col2:
        subverticals = df[df['startup'] == startup]['subvertical'].unique().tolist()
        st.metric('SubIndustry', ', '.join(map(str, subverticals)))
    with col3:
        city = df[df['startup'] == startup]['city'].unique().tolist()
        st.metric('Location', ', '.join(map(str, city)))

    st.header('Funding Details')
    st.dataframe(df[df['startup']==startup][['investors','round','amount']])


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    load_general_analysis()
elif option == 'Startup':
    startUp = st.sidebar.selectbox('select startup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
    if btn1:
        load_startup_analysis(startUp)


else:
    Investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    st.title('Investor Analysis')
    if btn2:
        load_investor_details(Investor)
