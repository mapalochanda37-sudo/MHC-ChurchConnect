import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
from database1_neon import create_table,get_all_departments,save_department,create_departments_table,create_member_departments_table,save_member, create_departments_table,get_all_members, search_member, create_transactions_table, get_total_income_this_month, save_transactions, get_all_transactions, get_member_transactions,create_events_table,save_event,get_upcoming_events,get_all_events,assign_member_to_department,get_new_members_this_month

st.set_page_config(
    page_title='MHC ChurchConnect',
    page_icon='⛪',
    layout='wide'
)
# reset_all_data()
create_table()
create_events_table()
create_transactions_table()
create_departments_table()
create_member_departments_table()

st.sidebar.image('mhc_logo.png')
password = st.sidebar.text_input('Admin Password', type='password')
if password != 'MHC2026':
    st.warning('Please enter the admin password to access the system.')
    st.stop()

st.title('⛪ChurchConnect')
st.caption('Engineering a Smarter World — MHC Engineering Solutions Zambia')
st.divider()

st.sidebar.title('Church Management Panel')
st.sidebar.divider()
page = st.sidebar.selectbox('Page' , ['Dashboard', 'Members','Tithes & Offerings','Events','Departments'])

if page == 'Members':
    total = len(get_all_members())
    st.metric('Total Members', total)

    st.header('Add New Member')
    full_name = st.text_input('Full Name')
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    birthday = st.text_input("Birthday (YYYY-MM-DD)")
    date_joined = st.text_input("Date Joined (YYYY-MM-DD)")
    baptised = st.selectbox("Baptised", ['Yes', 'No'])
    marital_status = st.selectbox("Marital Status",['Single','Married','Divorced','Widowed'])
    status = st.selectbox("Status", ["Active", "Inactive"])

    if st.button("Save Member"):
        if not full_name or not phone or not address or not baptised or not marital_status or not status:
            st.warning('Please fill in the required fields!')
        else:
            save_member(
                full_name,
                phone,
                email,
                address,
                birthday,
                date_joined,
                baptised,
                marital_status,
                status
            )
            st.success("Member saved successfully!")

    st.divider()

    st.header('View Members')

    search = st.text_input('Search by name or phone')

    if search:
        members = search_member(search)
    else:
        members = get_all_members()

    if members:
        df = pd.DataFrame(
            members,
            columns=["ID","Full Name","Phone","Email","Address","Birthday","Date Joined","Baptised","Marital Status","Status"]
        )
        st.dataframe(df)
    else:
        st.info('No members were found in the database')

elif page == 'Tithes & Offerings':
    totals = get_total_income_this_month()
    st.metric('Total Income This Month', f'K{totals: .2f}')

    st.header('Add Member Contribution')

    members = get_all_members()
    member_names = [m[1] for m in members]
    selected_name = st.selectbox('Select Member', member_names)

    selected_member = [m for m in members if m[1] == selected_name][0]
    member_id = selected_member[0]

    amount = st.number_input('Amount')
    transaction_type = st.selectbox('Type',['Tithe','Offering','Building Fund','Missions','Bus Project','Camp Meeting'])
    date = st.date_input('Date')
    notes = st.text_input('Notes')

    if st.button('Save'):
        if selected_member == '':
            st.warning('No User Input, Please select a member')
        else:
            save_transactions(member_id,amount,transaction_type,date,notes)
            st.success('Contributions saved successfully')

    st.divider()

    st.header('View All Transactions')

    total_transactions = get_all_transactions()

    if total_transactions:
        log = pd.DataFrame(
            total_transactions,
            columns=['ID','Member_ID','Amount','Transaction_Type','Date','Notes']
        )
        st.dataframe(log)
    else:
        st.info('No Transactions Available')

    st.divider()

    st.header('Member Giving History')

    select_member = st.selectbox('Select Member for History', member_names)
    selected_for_history = [m for m in members if m[1] == select_member][0]
    history_id = selected_for_history[0]

    member_transactions = get_member_transactions(history_id)

    if member_transactions:
        history_df = pd.DataFrame(
            member_transactions,
            columns=['ID','Member ID','Amount','Type','Date','Notes']
        )
        st.dataframe(history_df)
    else:
        st.info('No transactions found for this member')

elif page == 'Events':
    st.header('Create New Event')

    event_name = st.text_input('Event Name')
    venue = st.text_input('Venue')
    event_date = st.date_input('Date')
    event_time = st.time_input('Time')
    person_in_charge = st.text_input('Person in Charge')
    description = st.text_input('Event Description')

    if st.button('Save Event'):
        if not event_name or not venue or not event_date or not event_time or not person_in_charge:
            st.warning('Please fill in all the required fields!')
        else:
            event_date = event_date.strftime("%Y-%m-%d")
            event_time = event_time.strftime("%H:%M:%S")
            save_event(event_name,venue,event_date,event_time,person_in_charge,description)
            st.success('Event Created Successfully!')

    st.divider()

    st.header('Upcoming Events')

    upcoming_events = get_upcoming_events()

    if upcoming_events:
        log1 = pd.DataFrame(
            upcoming_events,
            columns=['ID','Event_Name','Venue','Event_Date','Event_Time','Person_in_Charge','Description','created_date']
        )
        st.dataframe(log1)
    else:
        st.info('No Upcoming Events.')

    st.divider()

    st.header('All Events')

    all_events = get_all_events()

    if all_events:
        log2 = pd.DataFrame(
            all_events,
            columns=['ID','Event Name','Venue','Event_Date','Event_Time','Person in Charge','Description','Created Date']
        )
        st.dataframe(log2)

elif page == 'Departments':
    st.header('Create Department')

    name = st.text_input('Department Name')
    chairperson = st.text_input('Chairperson')
    secretary = st.text_input('Secretary')
    treasurer = st.text_input('Treasurer')

    if st.button('Save Department'):
        if not name or not chairperson:
            st.warning('Please fill in all the required fields!')
        else:
            save_department(name,chairperson, secretary, treasurer)
            st.success('Department Created Successfully!')

    st.divider()

    st.header('Assign member to department(s)')

    members = get_all_members()
    member_dict = {m[1]: m[0] for m in members}

    departments = get_all_departments()
    department_dict = {d[1]: d[0] for d in departments}

    selected_member = st.selectbox("Select Member",member_dict.keys())
    selected_department = st.selectbox('Select Department', department_dict.keys())

    if st.button("Assign Member"):
        member_id = member_dict[selected_member]
        department_id = department_dict[selected_department]
        try:
            assign_member_to_department(member_id, department_id)
            st.success("Member assigned successfully!")
        except:
            st.warning("This member is already assigned to that department.")

elif page == 'Dashboard':
    st.title('ChurchConnect Dashboard')
    st.divider()

    all_members = get_all_members()
    new_members = get_new_members_this_month()
    total_income = get_total_income_this_month()
    upcoming = get_upcoming_events()

    active_members = [m for m in all_members if m[9] == 'Active']

    today = datetime.now().date()
    week_later = today + timedelta(days=7)

    events_this_week = [
        e for e in upcoming
        if today <= datetime.strptime(e[3], "%Y-%m-%d").date() <= week_later
    ]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Members", len(active_members))
    with col2:
        st.metric("New Members This Month", len(new_members))
    with col3:
        st.metric("Total Income This Month", f"K {total_income:,.2f}")
    with col4:
        st.metric("Events This Week", len(events_this_week))

    st.divider()

    st.subheader("Monthly Income")

    all_transactions = get_all_transactions()

    if all_transactions:
        df_trans = pd.DataFrame(all_transactions, columns=[
            'id','member_id','amount','transaction_type','date','notes'
        ])
        df_trans['month'] = pd.to_datetime(df_trans['date']).dt.to_period('M').astype(str)
        monthly = df_trans.groupby('month')['amount'].sum().reset_index()
        monthly.columns = ['Month','Total Income (K)']
        st.bar_chart(monthly.set_index('Month'))
    else:
        st.info("No transactions recorded yet.")

    st.divider()

    st.subheader("Birthdays This Week")

    birthday_list = []

    for m in all_members:
        try:
            bday = datetime.strptime(m[5], "%Y-%m-%d")
            bday_this_year = bday.replace(year=today.year)
            if today <= bday_this_year.date() <= week_later:
                birthday_list.append({'Name': m[1],'Phone': m[2],'Birthday': m[5]})
        except:
            pass

    if birthday_list:
        st.dataframe(pd.DataFrame(birthday_list))
    else:
        st.info("No birthdays this week.")

    st.divider()

    st.subheader("Pastoral Concern — Not Given in 30 Days ")

    thirty_days_ago = today - timedelta(days=30)

    recent_givers = set()

    for t in all_transactions:
        try:
            t_date = datetime.strptime(t[4], "%Y-%m-%d").date()
            if t_date >= thirty_days_ago:
                recent_givers.add(t[1])
        except:
            pass

    concern_list = []

    for m in active_members:
        if m[0] not in recent_givers:
            concern_list.append({'Name': m[1],'Phone': m[2],'Email': m[3]})

    if concern_list:
        st.dataframe(pd.DataFrame(concern_list))
    else:
        st.success("All active members have given in the last 30 days!")

    st.divider()

    st.subheader("Reports")

    def generate_member_list_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("MHC ChurchConnect", styles['Title']))
        story.append(Paragraph("Member List Report", styles['Heading2']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        members = get_all_members()
        data = [['Name', 'Phone', 'Email', 'Status', 'Date Joined']]
        for m in members:
            data.append([m[1], m[2], m[3], m[9], m[6]])
        table = Table(data, colWidths=[130, 90, 150, 70, 90])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F3F4')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(table)
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_income_summary_pdf():
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("MHC ChurchConnect", styles['Title']))
        story.append(Paragraph("Monthly Income Summary", styles['Heading2']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        all_transactions = get_all_transactions()
        if all_transactions:
            df = pd.DataFrame(all_transactions, columns=[
                'id','member_id','amount','transaction_type','date','notes'
            ])
            df['month'] = pd.to_datetime(df['date']).dt.to_period('M').astype(str)
            monthly = df.groupby('month')['amount'].sum().reset_index()
            data = [['Month', 'Total Income (K)']]
            for _, row in monthly.iterrows():
                data.append([row['month'], f"K {row['amount']:,.2f}"])
            table = Table(data, colWidths=[200, 200])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F3F4')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No transactions recorded yet.", styles['Normal']))
        doc.build(story)
        buffer.seek(0)
        return buffer

    def generate_giving_statement_pdf(member_id, member_name):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        story.append(Paragraph("MHC ChurchConnect", styles['Title']))
        story.append(Paragraph(f"Giving Statement — {member_name}", styles['Heading2']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
        story.append(Spacer(1, 20))
        transactions = get_member_transactions(member_id)
        if transactions:
            data = [['Date', 'Type', 'Amount (K)', 'Notes']]
            total = 0
            for t in transactions:
                data.append([t[4], t[3], f"K {t[2]:,.2f}", t[5]])
                total += t[2]
            data.append(['', 'TOTAL', f"K {total:,.2f}", ''])
            table = Table(data, colWidths=[100, 120, 110, 170])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F2F3F4')),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("No transactions found for this member.", styles['Normal']))
        doc.build(story)
        buffer.seek(0)
        return buffer

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download Member Transactions",
            data=generate_member_list_pdf(),
            file_name="member_list.pdf",
            mime="application/pdf"
        )

    with col2:
        st.download_button(
            label="Download Income Summary PDF",
            data=generate_income_summary_pdf(),
            file_name="income_summary.pdf",
            mime="application/pdf"
        )

    st.subheader("Member Giving Statement")

    all_members = get_all_members()
    member_dict = {m[1]: (m[0]) for m in all_members}
    selected = st.selectbox("Select Member", member_dict.keys(), key="pdf_member")

    if st.button("Generate Giving Statement"):
        mid = member_dict[selected]
        pdf = generate_giving_statement_pdf(mid, selected)
        st.download_button(
            label="Download Statement PDF",
            data=pdf,
            file_name=f"{selected}_giving_statement.pdf",
            mime="application/pdf"
        )

    st.divider()

    st.subheader("Annual Giving Summary")

    year_selected = st.selectbox(
        "Select Year",
        [str(y) for y in range(2024, datetime.now().year + 1)],
        key="annual_year"
    )

    all_transactions = get_all_transactions()

    if all_transactions:
        df = pd.DataFrame(all_transactions, columns=[
            'id', 'member_id', 'amount', 'transaction_type', 'date', 'notes'
        ])
        df['year'] = pd.to_datetime(df['date']).dt.year.astype(str)
        df_year = df[df['year'] == year_selected]
        summary = df_year.groupby('member_id')['amount'].sum().reset_index()
        summary.columns = ['member_id', 'total_given']
        member_dict = {m[0]: m[1] for m in all_members}
        summary['Member Name'] = summary['member_id'].map(member_dict)
        summary = summary[['Member Name', 'total_given']].sort_values(
            'total_given', ascending=False
        )
        summary.columns = ['Member Name', 'Total Given (K)']
        summary['Total Given (K)'] = summary['Total Given (K)'].apply(
            lambda x: f"K {x:,.2f}"
        )
        st.dataframe(summary)

        if st.button("Download Annual Summary PDF"):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            story.append(Paragraph("MHC ChurchConnect", styles['Title']))
            story.append(Paragraph(f"Annual Giving Summary — {year_selected}", styles['Heading2']))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y')}", styles['Normal']))
            story.append(Spacer(1, 20))
            data = [['Member Name', 'Total Given (K)']]
            for _, row in summary.iterrows():
                data.append([row['Member Name'], row['Total Given (K)']])
            table = Table(data, colWidths=[300, 150])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F3F4')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(table)
            doc.build(story)
            buffer.seek(0)
            st.download_button(
                label="Click to Download",
                data=buffer,
                file_name=f"annual_giving_summary_{year_selected}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("No transactions recorded yet.")

    st.divider()

    st.subheader("Data Backup 💾")

    col1, col2, col3 = st.columns(3)

    with col1:
        members_df = pd.DataFrame(get_all_members(), columns=[
            'ID','Full Name','Phone','Email','Address',
            'Birthday','Date Joined','Baptised','Marital Status','Status'
        ])
        st.download_button(
            label="Backup Members",
            data=members_df.to_csv(index=False),
            file_name="members.csv",
            mime="text/csv"
        )

    with col2:
        trans_df = pd.DataFrame(get_all_transactions(), columns=[
            'ID','Member ID','Amount','Transaction Type','Date','Notes'
        ])
        st.download_button(
            label="Backup Transactions",
            data=trans_df.to_csv(index=False),
            file_name="transactions.csv",
            mime="text/csv"
        )

    with col3:
        events_df = pd.DataFrame(get_all_events(), columns=[
            'ID','Event Name','Venue','Date','Time',
            'Person in Charge','Description','Created Date'
        ])
        st.download_button(
            label="Backup Events",
            data=events_df.to_csv(index=False),
            file_name="events.csv",
            mime="text/csv"
        )

    st.divider()
st.markdown("""
    <hr>
    <p style='text-align: center; color: grey; font-size: 12px;'>
        © 2026 ChurchConnect Pro | MHC Technologies Zambia<br>
        Church Management System • Built for Modern Ministries
    </p>
""", unsafe_allow_html=True)