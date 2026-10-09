import React, { useEffect, useMemo, useRef, useState } from "react";
import { fetchHealth, postChat } from "./api";
import {
  Activity, AlertCircle, ArrowDownRight, ArrowRight, ArrowUpRight,
  BarChart3, Bell, BookOpen, Bot, BrainCircuit, Check, CheckCircle2,
  ChevronDown, Clock3, Database, FileText, Headphones, Inbox, LayoutDashboard,
  Menu, MessageSquare, MoreHorizontal, Plus, Search, Send, Server, Settings,
  ShieldCheck, Sparkles, Ticket, TrendingUp, UserRound, Wifi, X, Zap
} from "lucide-react";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/$/, "");

const NAV_ITEMS = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "Live Chat", icon: MessageSquare },
  { label: "Tickets", icon: Ticket },
  { label: "Knowledge Base", icon: BookOpen },
  { label: "Analytics", icon: BarChart3 },
  { label: "Settings", icon: Settings },
];

// Clearly labelled demo records. Connect a ticket-list API before using these operationally.
const DEMO_TICKETS = [
  { id: "T-1048", title: "Payment deducted, order failed", customer: "Aarav Sharma", intent: "Payment", priority: "High", status: "Open", time: "2 min ago" },
  { id: "T-1047", title: "Warranty claim for laptop", customer: "Priya Verma", intent: "Warranty", priority: "Medium", status: "In progress", time: "12 min ago" },
  { id: "T-1046", title: "Unable to reset password", customer: "Rahul Singh", intent: "Account", priority: "Low", status: "Resolved", time: "24 min ago" },
  { id: "T-1045", title: "Product overheating", customer: "Neha Gupta", intent: "Technical", priority: "High", status: "Escalated", time: "31 min ago" },
  { id: "T-1044", title: "Track my shipment", customer: "Kabir Mehta", intent: "Shipping", priority: "Low", status: "Resolved", time: "45 min ago" },
];

const FAQS = [
  { id: "FAQ001", category: "Refund", question: "How can I request a refund?", answer: "You can request a refund within 30 days of purchase through the customer portal, subject to the refund policy conditions." },
  { id: "FAQ002", category: "Refund", question: "How long does a refund take?", answer: "Approved refunds are normally processed within 5 to 7 business days." },
  { id: "FAQ003", category: "Order tracking", question: "How can I track my order?", answer: "You can track your order using the tracking number available in your account." },
  { id: "FAQ007", category: "Warranty", question: "How long is the product warranty?", answer: "The standard product warranty is valid for 12 months from the purchase date." },
  { id: "FAQ009", category: "Payment", question: "What payment methods are supported?", answer: "We support credit cards, debit cards, UPI, and selected online payment methods." },
  { id: "FAQ014", category: "Account", question: "How can I reset my password?", answer: "Use the Forgot Password option on the login page and follow the instructions sent to your registered email." },
];

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

export default function App() {
  const [page, setPage] = useState("Overview");
  const [mobileNav, setMobileNav] = useState(false);
  const [search, setSearch] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const [toast, setToast] = useState("");
  const [chatInput, setChatInput] = useState("");
  const [priority, setPriority] = useState("medium");
  const [sending, setSending] = useState(false);
  const [ticketFilter, setTicketFilter] = useState("All");
  const [expandedFaq, setExpandedFaq] = useState("FAQ002");
  const [conversationId] = useState(() => `WEB-${Date.now()}`);
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hi! I'm your AI support assistant. I can help with refunds, shipping, payments, warranties, and order questions. What can I help you with today?",
      time: "Ready",
    },
  ]);
  const messagesEnd = useRef(null);
  const toastTimer = useRef(null);

  useEffect(() => {
    checkHealth();
    return () => window.clearTimeout(toastTimer.current);
    // one health check when the UI loads
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sending]);

  async function checkHealth() {
  setApiStatus("checking");

  try {
    await fetchHealth();
    setApiStatus("online");
  } catch (error) {
    console.error("Backend health check failed:", error);
    setApiStatus("offline");
  }
}

  function notify(message) {
    setToast(message);
    window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(() => setToast(""), 3000);
  }

  async function sendMessage(value = chatInput) {
    const text = value.trim();
    if (!text || sending) return;

    setMessages((old) => [...old, { role: "user", text, time: timeNow() }]);
    setChatInput("");
    setSending(true);

    try {
      const data = await postChat({
  customer_id: "WEB-C001",
  conversation_id: conversationId,
  message: text,
  priority,
});

setApiStatus("online");

setMessages((old) => [
  ...old,
  {
    role: "assistant",
    text: data.response || "Your request was processed.",
    time: new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    }),
    intent: data.intent,
    action: data.agent_action,
    confidence: data.confidence,
  },
]);
    } catch (error) {
      setApiStatus("offline");
      setMessages((old) => [...old, {
        role: "assistant",
        text: `I couldn't reach the support API. ${error.message}. Check that FastAPI is running and the API URL is configured correctly.`,
        time: "Connection issue",
        error: true,
      }]);
    } finally {
      setSending(false);
    }
  }

  const filteredTickets = useMemo(() => DEMO_TICKETS.filter((item) => {
    const query = search.toLowerCase();
    const matchesSearch = `${item.id} ${item.title} ${item.customer} ${item.intent}`.toLowerCase().includes(query);
    return matchesSearch && (ticketFilter === "All" || item.status === ticketFilter);
  }), [search, ticketFilter]);

  const filteredFaqs = useMemo(() => FAQS.filter((item) =>
    `${item.id} ${item.category} ${item.question} ${item.answer}`.toLowerCase().includes(search.toLowerCase())
  ), [search]);

  function openPage(name) {
    setPage(name);
    setMobileNav(false);
    setSearch("");
  }

  return (
    <div className="app-shell">
      {mobileNav && <button className="mobile-scrim" onClick={() => setMobileNav(false)} aria-label="Close navigation" />}
      <aside className={`sidebar ${mobileNav ? "sidebar-open" : ""}`}>
        <div className="brand-row">
          <div className="brand-mark"><BrainCircuit size={23} /></div>
          <div><div className="brand-name">AI<span>Support</span></div><div className="brand-caption">INTELLIGENT SERVICE</div></div>
          <button className="icon-button mobile-close" onClick={() => setMobileNav(false)} aria-label="Close menu"><X size={18} /></button>
        </div>
        <div className="workspace-switcher">
          <div className="workspace-avatar">AC</div><div className="workspace-copy"><strong>Acme Commerce</strong><span>Support workspace</span></div><ChevronDown size={16} className="muted-icon" />
        </div>
        <div className="nav-label">WORKSPACE</div>
        <nav className="navigation">
          {NAV_ITEMS.map(({ label, icon: Icon }) => <button key={label} onClick={() => openPage(label)} className={`nav-item ${page === label ? "nav-active" : ""}`}><Icon size={18} strokeWidth={1.8} /><span>{label}</span>{label === "Tickets" && <span className="nav-count">5</span>}{label === "Live Chat" && <span className="live-dot" />}</button>)}
        </nav>
        <div className="sidebar-bottom">
          <div className="usage-card"><div className="usage-icon"><Sparkles size={16} /></div><strong>AI assistant</strong><p>RAG-powered answers with smart escalation.</p><div className="usage-track"><span /></div><div className="usage-foot"><span>Knowledge sources</span><b>FAQ index</b></div></div>
          <button className="profile-row" onClick={() => openPage("Settings")}><div className="profile-avatar">KP</div><div className="profile-copy"><strong>Workspace Admin</strong><span>Administrator</span></div><MoreHorizontal size={18} className="muted-icon" /></button>
        </div>
      </aside>

      <main className="main-shell">
        <header className="topbar">
          <div className="topbar-left"><button className="icon-button mobile-menu" onClick={() => setMobileNav(true)} aria-label="Open menu"><Menu size={20} /></button><div className="breadcrumbs"><span>Workspace</span><span className="crumb-slash">/</span><strong>{page}</strong></div></div>
          <div className="topbar-actions">
            <label className="global-search"><Search size={16} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search tickets or FAQs..." /><kbd>⌘ K</kbd></label>
            <button className={`api-pill ${apiStatus}`} onClick={checkHealth} title="Click to recheck API"><span className="api-dot" />{apiStatus === "online" ? "API connected" : apiStatus === "checking" ? "Checking API" : "API offline"}</button>
            <button className="icon-button notification-button" onClick={() => notify("You're all caught up.")} aria-label="Notifications"><Bell size={18} /><i /></button>
          </div>
        </header>

        <div className="page-content">
          {page === "Overview" && <OverviewPage openPage={openPage} apiStatus={apiStatus} />}
          {page === "Live Chat" && <ChatPage messages={messages} input={chatInput} setInput={setChatInput} sendMessage={sendMessage} sending={sending} priority={priority} setPriority={setPriority} apiStatus={apiStatus} messagesEnd={messagesEnd} />}
          {page === "Tickets" && <TicketsPage tickets={filteredTickets} filter={ticketFilter} setFilter={setTicketFilter} notify={notify} />}
          {page === "Knowledge Base" && <KnowledgePage faqs={filteredFaqs} expandedFaq={expandedFaq} setExpandedFaq={setExpandedFaq} notify={notify} />}
          {page === "Analytics" && <AnalyticsPage />}
          {page === "Settings" && <SettingsPage apiStatus={apiStatus} checkHealth={checkHealth} notify={notify} />}
        </div>
        <footer className="app-footer"><span><span className="footer-status" /> Intelligent support workspace</span><span>SupportIQ <b>·</b> React + FastAPI</span></footer>
      </main>
      {toast && <div className="toast"><CheckCircle2 size={17} />{toast}</div>}
    </div>
  );
}

function PageHeading({ eyebrow, title, subtitle, action }) {
  return <div className="page-heading"><div><div className="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{subtitle}</p></div>{action && <div className="heading-action">{action}</div>}</div>;
}

function MetricCard({ icon: Icon, label, value, change, positive = true, foot, color }) {
  return <div className="metric-card"><div className="metric-top"><div className={`metric-icon ${color}`}><Icon size={19} /></div><span className={`metric-change ${positive ? "positive" : "negative"}`}>{positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}{change}</span></div><div className="metric-label">{label}</div><div className="metric-value">{value}</div><div className="metric-foot">{foot}</div></div>;
}

function OverviewPage({ openPage, apiStatus }) {
  const volume = [34, 46, 41, 63, 54, 69, 49, 76, 66, 86, 71, 94];
  return <>
    <PageHeading eyebrow="OVERVIEW / YOUR WORKSPACE" title="Your support command center" subtitle="Monitor AI conversations, explore knowledge, and review sample support activity." action={<button className="primary-button" onClick={() => openPage("Live Chat")}><Plus size={17} /> New conversation</button>} />
    <div className="welcome-banner"><div className="welcome-orb"><BrainCircuit size={28} /></div><div className="welcome-copy"><div className="welcome-kicker"><span /> AI SUPPORT ENGINE</div><h2>Let AI handle the busywork.</h2><p>Answer customer questions with RAG, route intents intelligently, and identify cases that need human support.</p></div><button className="welcome-button" onClick={() => openPage("Live Chat")}>Try AI assistant <ArrowRight size={16} /></button><div className="banner-decoration decoration-one" /><div className="banner-decoration decoration-two" /></div>
    <div className="section-heading"><div><h2>Support at a glance</h2><p>Illustrative values, not production telemetry</p></div><span className="demo-tag">SAMPLE DATA</span></div>
    <div className="metrics-grid"><MetricCard icon={MessageSquare} label="Conversations" value="1,284" change="12.8%" foot="illustrative activity" color="purple" /><MetricCard icon={CheckCircle2} label="AI resolution rate" value="78.6%" change="8.2%" foot="sample estimate" color="green" /><MetricCard icon={Clock3} label="Avg. response time" value="1.8s" change="14.4%" foot="sample estimate" color="blue" /><MetricCard icon={Ticket} label="Open tickets" value="24" change="3.1%" positive={false} foot="not from live ticket API" color="orange" /></div>
    <div className="dashboard-grid"><section className="surface chart-panel"><div className="panel-heading"><div><h3>Conversation volume</h3><p>Example activity across 12 periods</p></div><span className="source-label">DEMO</span></div><div className="chart-legend"><span><i className="legend-purple" /> Conversations</span><span className="legend-muted">Illustrative trend</span></div><div className="bar-chart">{volume.map((height, index) => <div className="bar-column" key={index}><div className="chart-bar" style={{ height: `${height}%` }} /><span>{["M","T","W","T","F","S","S","M","T","W","T","F"][index]}</span></div>)}</div><div className="chart-footer"><span><i className="legend-purple" /> Total conversations</span><strong>1,284 <small><TrendingUp size={13} /> 12.8%</small></strong></div></section>
      <section className="surface intent-panel"><div className="panel-heading"><div><h3>Top customer intents</h3><p>Sample intent mix</p></div><button className="icon-button" onClick={() => openPage("Analytics")} aria-label="View analytics"><MoreHorizontal size={18} /></button></div><div className="intent-list">{[["Refund requests",76,"#7767EC"],["Order tracking",64,"#38A88D"],["Technical issues",43,"#E6A24B"],["Payments",31,"#5798E7"],["Account access",22,"#D37BB3"]].map(([label,width,color]) => <div className="intent-row" key={label}><div className="intent-label"><span>{label}</span><b>{width}%</b></div><div className="intent-track"><span style={{ width: `${width}%`, background: color }} /></div></div>)}</div><button className="text-button full-width" onClick={() => openPage("Analytics")}>Explore analytics <ArrowRight size={15} /></button></section></div>
    <section className="surface recent-panel"><div className="panel-heading"><div><h3>Recent support activity</h3><p>Illustrative ticket records</p></div><button className="text-button" onClick={() => openPage("Tickets")}>View tickets <ArrowRight size={15} /></button></div><TicketTable tickets={DEMO_TICKETS.slice(0,4)} /></section>
    <div className="status-note"><div className={`status-note-icon ${apiStatus}`}><Activity size={17} /></div><div><strong>Backend connectivity</strong><p>{apiStatus === "online" ? "FastAPI health endpoint is reachable." : apiStatus === "checking" ? "Checking FastAPI health endpoint." : "Start FastAPI or configure VITE_API_BASE_URL to enable live chat."}</p></div><span className={`status-label ${apiStatus}`}>{apiStatus === "online" ? "Connected" : apiStatus === "checking" ? "Checking" : "Offline"}</span></div>
  </>;
}

function ChatPage({ messages, input, setInput, sendMessage, sending, priority, setPriority, apiStatus, messagesEnd }) {
  const prompts = ["How long does a refund take?", "Where is order ORD1001?", "I forgot my password"];
  return <>
    <PageHeading eyebrow="AI WORKSPACE / CONVERSATIONS" title="Live AI chat" subtitle="Send a message to your deployed FastAPI + RAG + Agentic AI pipeline." action={<span className={`api-pill ${apiStatus}`}><span className="api-dot" />{apiStatus === "online" ? "Connected" : apiStatus === "checking" ? "Checking" : "Backend offline"}</span>} />
    <div className="chat-layout"><aside className="chat-info-rail"><div className="rail-title"><span>CONVERSATION</span><button className="icon-button" onClick={() => window.location.reload()} title="Start a fresh session"><Plus size={17} /></button></div><div className="current-conversation"><div className="conversation-icon"><Sparkles size={18} /></div><div><strong>AI conversation</strong><span>Support assistant</span></div><span className="live-dot" /></div><div className="rail-divider" /><div className="rail-label">QUICK PROMPTS</div>{prompts.map((item) => <button className="quick-prompt" key={item} disabled={sending} onClick={() => sendMessage(item)}>{item}<ArrowUpRight size={14} /></button>)}<div className="rail-spacer" /><div className="rail-tip"><ShieldCheck size={19} /><strong>Grounded answers</strong><p>The backend retrieves knowledge from the configured FAQ index before generating a response.</p></div></aside>
      <section className="chat-window"><div className="chat-topline"><div className="bot-avatar"><Bot size={19} /></div><div className="chat-agent-name"><strong>SupportIQ Assistant</strong><span><i /> AI customer support</span></div><div className="chat-top-actions"><span className="privacy-label"><ShieldCheck size={14} /> Session</span><button className="icon-button" onClick={() => notifyTextCopy()} title="Session info"><MoreHorizontal size={18} /></button></div></div>
        <div className="message-stream"><div className="conversation-date"><span /> CURRENT SESSION <span /></div>{messages.map((message,index) => <div className={`message-row ${message.role === "user" ? "message-user" : ""}`} key={`${index}-${message.time}`}>
          {message.role === "assistant" && <div className="message-avatar"><Bot size={15} /></div>}<div className="message-content"><div className="message-meta">{message.role === "user" ? "You" : "SupportIQ AI"} <span>{message.time}</span></div><div className={`message-bubble ${message.error ? "message-error" : ""}`}>{message.text}</div>{message.intent && <div className="message-tags"><span className="intent-chip"><Sparkles size={12} /> {message.intent}</span>{message.action && <span className="source-chip">{message.action.replaceAll("_"," ")}</span>}{typeof message.confidence === "number" && <span className="source-chip">{Math.round(message.confidence*100)}% confidence</span>}</div>}</div>{message.role === "user" && <div className="user-message-avatar"><UserRound size={15} /></div>}
        </div>)}{sending && <div className="message-row"><div className="message-avatar"><Bot size={15} /></div><div className="message-content"><div className="message-meta">SupportIQ AI <span>thinking</span></div><div className="message-bubble thinking"><i /><i /><i /></div></div></div>}<div ref={messagesEnd} /></div>
        <div className="suggestion-row"><span>TRY ASKING</span>{prompts.slice(0,2).map((item) => <button key={item} disabled={sending} onClick={() => sendMessage(item)}>{item}</button>)}</div>
        <form className="chat-composer" onSubmit={(event) => { event.preventDefault(); sendMessage(); }}><input value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask about refunds, shipping, orders..." disabled={sending} /><div className="composer-footer"><div className="composer-tools"><label className="priority-control">Priority <select value={priority} onChange={(event) => setPriority(event.target.value)}><option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option></select></label><span className="composer-hint"><ShieldCheck size={13} /> AI may make mistakes</span></div><button className="send-button" disabled={sending || !input.trim()} type="submit">{sending ? "Working..." : "Send"} <Send size={15} /></button></div></form>
      </section>
      <aside className="chat-context-rail"><div className="rail-title"><span>AI PIPELINE</span><span className="live-badge">INFO</span></div><Insight icon={BrainCircuit} color="violet" title="Intent intelligence" text="TF-IDF + Logistic Regression classifies customer queries." /><Insight icon={Database} color="mint" title="Knowledge retrieval" text="ChromaDB retrieves relevant FAQ documents for RAG." /><Insight icon={Zap} color="blue" title="Agentic routing" text="Routes knowledge questions, business tools, and escalations." /><div className="rail-divider" /><div className="rail-label">REQUEST CONTEXT</div><div className="context-row"><span>Customer</span><strong>WEB-C001</strong></div><div className="context-row"><span>Conversation</span><strong className="context-code">Current session</strong></div><div className="context-row"><span>Priority</span><span className={`priority-tag priority-${priority}`}>{priority}</span></div><div className="context-health"><span className={`api-dot ${apiStatus}`} /><span>Backend {apiStatus === "online" ? "connected" : apiStatus === "checking" ? "checking" : "offline"}</span></div><p className="context-disclaimer">Intent and action details appear after your backend responds.</p></aside>
    </div>
  </>;
}

function notifyTextCopy() {
  window.alert("Conversation memory is managed by the backend. This browser view uses one session ID.");
}

function Insight({ icon: Icon, color, title, text }) {
  return <div className="insight-card"><div className={`insight-icon ${color}`}><Icon size={19} /></div><div><strong>{title}</strong><p>{text}</p></div></div>;
}

function TicketTable({ tickets }) {
  return <div className="table-wrap"><table className="data-table"><thead><tr><th>TICKET</th><th>CUSTOMER / ISSUE</th><th>INTENT</th><th>PRIORITY</th><th>STATUS</th><th>UPDATED</th></tr></thead><tbody>{tickets.map((item) => <tr key={item.id}><td><strong className="ticket-id">{item.id}</strong></td><td><div className="ticket-title">{item.title}</div><div className="ticket-customer">{item.customer}</div></td><td><span className="category-chip">{item.intent}</span></td><td><span className={`priority-tag priority-${item.priority.toLowerCase()}`}><i />{item.priority}</span></td><td><span className={`status-tag status-${item.status.toLowerCase().replace(" ","-")}`}>{item.status}</span></td><td className="time-cell">{item.time}</td></tr>)}{tickets.length === 0 && <tr><td colSpan="6" className="empty-state">No tickets match the current filters.</td></tr>}</tbody></table></div>;
}

function TicketsPage({ tickets, filter, setFilter, notify }) {
  return <><PageHeading eyebrow="SUPPORT OPERATIONS / CASES" title="Support tickets" subtitle="Review the interface for case priority, status, and escalation." action={<button className="primary-button" onClick={() => notify("Ticket creation/listing needs a dedicated backend endpoint.")}><Plus size={17} /> Create ticket</button>} /><div className="metrics-grid compact-metrics"><MetricCard icon={Inbox} label="All tickets" value="05" change="Demo" foot="sample records" color="purple" /><MetricCard icon={AlertCircle} label="High priority" value="02" change="Demo" positive={false} foot="sample records" color="orange" /><MetricCard icon={Activity} label="In progress" value="01" change="Demo" foot="sample records" color="blue" /><MetricCard icon={CheckCircle2} label="Resolved" value="02" change="Demo" foot="sample records" color="green" /></div><section className="surface recent-panel"><div className="panel-heading table-toolbar"><div><h3>Support ticket preview</h3><p>Demo data — not connected to a ticket-list endpoint</p></div><div className="filter-group">{["All","Open","In progress","Resolved","Escalated"].map((item) => <button key={item} onClick={() => setFilter(item)} className={`filter-button ${filter===item?"filter-active":""}`}>{item}</button>)}</div></div><TicketTable tickets={tickets} /></section></>;
}

function KnowledgePage({ faqs, expandedFaq, setExpandedFaq, notify }) {
  return <><PageHeading eyebrow="KNOWLEDGE / RETRIEVAL" title="Knowledge base" subtitle="Browse a sample of the FAQ knowledge available to the RAG pipeline." action={<button className="primary-button" onClick={() => notify("Upload is a preview; add a document-ingestion API before enabling this action.")}><Plus size={17} /> Add source</button>} /><div className="kb-summary"><div className="kb-summary-icon"><Database size={22} /></div><div><strong>FAQ knowledge collection</strong><p>ChromaDB · Sentence Transformers embeddings · persisted vector index</p></div><span className="source-label">PREVIEW</span></div><div className="kb-search-hint"><Search size={17} /><span>Use the search box in the top bar to filter these FAQ records.</span><span>{faqs.length} shown</span></div><div className="faq-list">{faqs.map((faq) => <section className={`faq-card ${expandedFaq===faq.id?"faq-expanded":""}`} key={faq.id}><button className="faq-question" onClick={() => setExpandedFaq(expandedFaq===faq.id?"":faq.id)}><div className="faq-leading"><div className="faq-file"><FileText size={18} /></div><div><span className="faq-meta">{faq.id} <i /> {faq.category}</span><strong>{faq.question}</strong></div></div><ChevronDown size={18} className="faq-chevron" /></button>{expandedFaq===faq.id && <div className="faq-answer"><p>{faq.answer}</p><div><span className="source-chip">Sample FAQ record</span><button className="text-button" onClick={() => notify("Source metadata needs a knowledge-base endpoint.")}>Source details <ArrowUpRight size={14} /></button></div></div>}</section>)}{faqs.length===0 && <div className="surface empty-state">No FAQ records match your search.</div>}</div></>;
}

function AnalyticsPage() {
  const bars = [38,53,44,68,56,78,62,84,74,92,68,98];
  return <><PageHeading eyebrow="INSIGHTS / PERFORMANCE" title="Analytics & insights" subtitle="A visual starter for future request telemetry and model evaluation." action={<span className="source-label">SAMPLE DATA</span>} /><div className="metrics-grid"><MetricCard icon={MessageSquare} label="Conversations" value="1,284" change="12.8%" foot="demo metric" color="purple" /><MetricCard icon={ShieldCheck} label="Resolution rate" value="78.6%" change="8.2%" foot="demo metric" color="green" /><MetricCard icon={Clock3} label="Response latency" value="1.8s" change="14.4%" foot="demo metric" color="blue" /><MetricCard icon={TrendingUp} label="Customer rating" value="4.7/5" change="4.2%" foot="demo metric" color="orange" /></div><div className="dashboard-grid"><section className="surface chart-panel"><div className="panel-heading"><div><h3>Conversation trend</h3><p>12 illustrative periods</p></div><span className="category-chip">Demo</span></div><div className="bar-chart analytics-bars">{bars.map((height,index)=><div className="bar-column" key={index}><div className="chart-bar" style={{height:`${height}%`}}/><span>{index+1}</span></div>)}</div><div className="chart-footer"><span>Illustrative volume</span><strong>Not live telemetry</strong></div></section><section className="surface intent-panel"><div className="panel-heading"><div><h3>Intent breakdown</h3><p>Sample query categories</p></div></div><div className="intent-list">{[["Refund",29],["Order tracking",24],["Technical",18],["Payment",16],["Account / other",13]].map(([name,value])=><div className="intent-row" key={name}><div className="intent-label"><span>{name}</span><b>{value}%</b></div><div className="intent-track"><span style={{width:`${value}%`}}/></div></div>)}</div></section></div><div className="status-note"><div className="status-note-icon violet"><BarChart3 size={17}/></div><div><strong>Next analytics integration</strong><p>Capture request latency, predicted intent, retrieval relevance, escalation rate, and feedback in persistent telemetry.</p></div></div></>;
}

function SettingsPage({ apiStatus, checkHealth, notify }) {
  return <><PageHeading eyebrow="WORKSPACE / CONFIGURATION" title="Settings" subtitle="Inspect API connectivity, core components, and the production checklist." /><div className="settings-grid"><section className="surface settings-card"><div className="settings-section-head"><div className="settings-icon purple"><Server size={19}/></div><div><h3>Backend connection</h3><p>Checked through your FastAPI health endpoint.</p></div></div><div className="settings-row"><div><strong>API health</strong><span>GET /health</span></div><span className={`status-tag status-${apiStatus==="online"?"resolved":apiStatus==="checking"?"in-progress":"open"}`}>{apiStatus}</span></div><div className="settings-row"><div><strong>Chat endpoint</strong><span>POST /chat</span></div><span className="status-tag status-resolved">Configured</span></div><button className="secondary-button" onClick={checkHealth}><Wifi size={16}/> Test API connection</button></section><section className="surface settings-card"><div className="settings-section-head"><div className="settings-icon green"><BrainCircuit size={19}/></div><div><h3>AI architecture</h3><p>Configured components in your prototype.</p></div></div>{[["Intent classifier","TF-IDF + Logistic Regression"],["Vector database","ChromaDB"],["Embeddings","Sentence Transformers"],["LLM provider","Groq API"],["Agent routing","Python intent router"]].map(([name,value])=><div className="settings-row" key={name}><div><strong>{name}</strong><span>{value}</span></div><CheckCircle2 size={17} className="setting-check"/></div>)}</section><section className="surface settings-card settings-wide"><div className="settings-section-head"><div className="settings-icon orange"><ShieldCheck size={19}/></div><div><h3>Production readiness</h3><p>Recommended before opening the service to public users.</p></div></div>{["Keep API keys on the backend; never include provider keys in VITE_ variables.","Add authentication and rate limiting to POST /chat.","Enable HTTPS for the API and configure CORS for the frontend origin.","Persist conversations and tickets in a database.","Authorize access before returning customer or order details."].map((text)=><div className="checklist-row" key={text}><Check size={17}/><span>{text}</span></div>)}</section></div><div className="settings-note"><AlertCircle size={17}/><span>This screen displays configuration guidance; it does not modify backend settings.</span></div></>;
}
