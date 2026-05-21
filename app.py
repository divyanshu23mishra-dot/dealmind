import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from memory_module import get_memories, store_memory, get_memories_list, route_query

# Environment variables load karna (.env aur Streamlit Secrets dono ko support karta hai) [cite: 806-807]
load_dotenv()
GROQ_API_KEY = st.secrets.get('GROQ_API_KEY', os.getenv('GROQ_API_KEY', ''))

# Page configuration [cite: 721-722]
st.set_page_config(page_title='DealMind', page_icon='🎬', layout='wide')

# Session States Initialize karna (Pehle check karna mandatory hai) [cite: 760-761, 944]
if 'prospect' not in st.session_state:
    st.session_state['prospect'] = 'Sarah'
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'query_log' not in st.session_state:
    st.session_state['query_log'] = []

# Prospect static data dict [cite: 743-744]
prospects = {
    'Sarah': {'company': 'Acme Corp', 'deal': '$200,000', 'stage': 'Negotiation', 'last_contact': '2 days ago', 'contact': 'Sarah Chen, VP Sales'}, [cite: 745-746]
    'Mark':  {'company': 'TechStart Inc', 'deal': '$45,000', 'stage': 'Discovery', 'last_contact': '5 days ago', 'contact': 'Mark Wilson, CEO'}, [cite: 747-748]
    'Priya': {'company': 'GlobalEdge', 'deal': '$85,000', 'stage': 'Proposal', 'last_contact': '1 day ago', 'contact': 'Priya Patel, Head of Ops'} [cite: 749-750]
}

# --- SIDEBAR DISPLAY ---
st.sidebar.markdown("<h1 style='color: #6c63ff; margin-bottom:0;'>🎬 DealMind</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#888; margin-top:0;'>AI Sales Intelligence</p>", unsafe_allow_html=True)
st.sidebar.markdown("### PROSPECTS")

# 3 Prospect Buttons
if st.sidebar.button('Sarah Chen  |  $200K  |  Negotiation'):
    st.session_state['prospect'] = 'Sarah'
if st.sidebar.button('Mark Wilson  |  $45K   |  Discovery'):
    st.session_state['prospect'] = 'Mark'
if st.sidebar.button('Priya Patel  |  $85K   |  Proposal'):
    st.session_state['prospect'] = 'Priya'

st.sidebar.markdown('---')
st.sidebar.markdown("### AI MEMORY PANEL")

# Hindsight se live dynamic memories display karna sidebar me [cite: 887-888]
current_prospect = st.session_state['prospect']
memories_list = get_memories_list(current_prospect)

if memories_list:
    st.sidebar.caption(f"✨ Memory: {len(memories_list)} items retrieved")
    for mem in memories_list:
        st.sidebar.markdown(f"- {mem}")
else:
    st.sidebar.info("No memories found.")

st.sidebar.markdown('---')
# Simulate New Session Button [cite: 905-906]
if st.sidebar.button('🔄 Simulate New Session'):
    st.session_state['chat_history'] = []
    st.rerun()

# --- MAIN AREA ---
# Top Header Banner [cite: 912-913]
st.markdown('''
<div style="background: linear-gradient(135deg, #6c63ff, #a855f7); padding: 20px 24px; border-radius: 12px; margin-bottom: 20px">
    <h2 style="color: white; margin: 0; font-size: 24px">DealMind AI Sales Platform</h2>
    <p style="color: #e8e4ff; margin: 4px 0 0; font-size: 14px">Persistent Context via Hindsight Memory Layer + Model Routing via CascadeFlow</p>
</div>
''', unsafe_allow_html=True) [cite: 914-920]

# Selected Prospect Profile Card
p_data = prospects[current_prospect]
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"### **{p_data['contact']}**") [cite: 754-755]
    col2.metric("Company", p_data['company']) [cite: 754-755]
    col3.metric("Deal Size", p_data['deal']) [cite: 754-755]
    col4.metric("Stage", p_data['stage']) [cite: 754-755]

st.markdown("---")

# --- BEFORE VS AFTER EMAIL PANEL --- [cite: 845-846]
st.subheader("💡 Email Personalization Impact Analysis")
b_col1, b_col2 = st.columns(2)

with b_col1:
    st.info("🔴 WITHOUT DealMind (Generic Follow-up)\n\n"
            "Subject: Following up on our conversation\n\n"
            "Hi Sarah,\nJust wanted to follow up on our conversation from last week. "
            "Please let me know if you have any questions. Happy to set up a call whenever works for you.\n\n"
            "Best,\n[Rep Name]") [cite: 216-224, 849-854]

with b_col2:
    st.success("🟢 WITH DealMind (Memory Powered) [⚡ Memory: 1.8s]\n\n"
               "Subject: Your June 30 go-live + one-pager for James\n\n"
               "Hi Sarah,\nFollowing up on our March 5 call. I know your June 30 go-live deadline is non-negotiable -- so I have put together an implementation plan that gets you live by June 15, giving you two weeks of buffer.\n\n"
               "I have also prepared a one-pager specifically for James Lee that shows the 3-month ROI case...\n\n"
               "Best,\n[Rep Name]") [cite: 225-237, 855-866]

# --- TABS: CHAT & COST DASHBOARD --- [cite: 757-758]
tab1, tab2 = st.tabs(['💬 Live Sales Assistant Chat', '📊 CascadeFlow Cost Dashboard'])

with tab1:
    # Chat History Display
    for message in st.session_state['chat_history']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # User Chat Input
    if user_input := st.chat_input(f"Ask DealMind about {current_prospect}..."):
        st.session_state['chat_history'].append({'role': 'user', 'content': user_input})
        with st.chat_message('user'):
            st.markdown(user_input)

        # 1. CascadeFlow Smart Routing Engine
        route = route_query(user_input)
        
        # 2. Hindsight Semantic Context Retrieval
        context_memory = get_memories(current_prospect, user_input)
        
        # Query log data save karna for dashboard
        st.session_state['query_log'].append({
            'query': user_input,
            'words': len(user_input.split()),
            'model': route['model'],
            'reason': route['reason'],
            'cost': route['cost']
        })

        # 3. System Prompt Customization
        system_prompt = f"""You are DealMind, an elite AI sales intelligence assistant.
Current prospect: {p_data['contact']} from {p_data['company']}.
Deal size: {p_data['deal']}. Stage: {p_data['stage']}.

{context_memory}

Use the memory context to give specific, personalized and action-oriented strategic advice. Maximum 150 words.""" [cite: 640-645, 779-782]

        # 4. Groq Inference Calling
        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model=route['model'], # CascadeFlow dynamic model
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': user_input}
                ],
                max_tokens=300
            )
            ai_reply = response.choices[0].message.content
            
            # 5. Continuous Learning: Store insight back to Hindsight
            store_memory(current_prospect, user_input, ai_reply)
            
            st.session_state['chat_history'].append({'role': 'assistant', 'content': ai_reply})
            st.rerun()
            
        except Exception as e:
            st.error(f"Groq API call fail ho gaya: {e}")

with tab2:
    # --- COST DASHBOARD DISPLAY ---
    logs = st.session_state['query_log']
    if not logs:
        st.info("Ask DealMind a question in the chat tab to initialize real-time cost tracking analytics.")
    else:
        total_queries = len(logs)
        actual_cost = sum(item['cost'] for item in logs)
        avg_cost = actual_cost / total_queries
        baseline_cost = total_queries * 0.008
        money_saved = baseline_cost - actual_cost
        pct_saved = (money_saved / baseline_cost) * 100 if baseline_cost > 0 else 0

        # Metrics Analytics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Queries Enacted", total_queries)
        m2.metric("Avg Cost / Query", f"${avg_cost:.5f}")
        m3.metric("Est. Without Routing", f"${baseline_cost:.4f}")
        m4.metric("Money Saved via CascadeFlow", f"${money_saved:.4f}", delta=f"{pct_saved:.1f}% Saved")

        st.markdown("### Detailed Model Routing Decisions")
        st.dataframe(logs, use_container_width=True)
        
        st.markdown("### Volume Share Per AI Model")
        model_counts = {}
        for item in logs:
            model_counts[item['model']] = model_counts.get(item['model'], 0) + 1
        st.bar_chart(model_counts)
        
        st.caption("⚡ System Optimized. Powered by CascadeFlow Router System.")
