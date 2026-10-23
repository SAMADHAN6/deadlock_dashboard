import streamlit as st
import pandas as pd
from copy import deepcopy

st.set_page_config(page_title="Deadlock & Banker’s Algorithm", page_icon="🔐", layout="wide")

st.markdown("""
<style>
/* Make numeric cells and matrix values easier to read */
[data-testid="stDataFrame"] [role="gridcell"] { font-size: 19px !important; }
[data-testid="stDataFrame"] [role="columnheader"] { font-size: 16px !important; }
[data-testid="stMetricValue"] { font-size: 30px !important; }
.big-number { font-size: 24px; font-weight: 750; letter-spacing: .3px; }
.sim-card { border: 1px solid rgba(128,128,128,.35); border-radius: 12px; padding: 12px; margin-bottom: 8px; }
.sim-title { font-size: 16px; font-weight: 700; }
.sim-sub { font-size: 13px; opacity: .8; }
</style>
""", unsafe_allow_html=True)

st.title("🔐 Deadlock Analysis & Resource Allocation Dashboard")
st.caption("Operating Systems Activity · Banker’s Algorithm · Deadlock Detection and Prevention")

DEFAULT_AVAILABLE = [3, 3, 2]
DEFAULT_ALLOCATION = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
DEFAULT_MAXIMUM = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
DEFAULT_RESOURCES = ["A (Printer)", "B (Scanner)", "C (Tape drive)"]

def need_matrix(maximum, allocation):
    return [[maximum[i][j] - allocation[i][j] for j in range(len(maximum[i]))]
            for i in range(len(maximum))]

def validate_state(available, allocation, maximum):
    if not available or not allocation or len(allocation) != len(maximum):
        return "Available, Allocation, and Max must contain matching data."
    m = len(available)
    if any(len(row) != m for row in allocation + maximum):
        return "Every Allocation and Max row must have the same number of resource types as Available."
    if any(not isinstance(x, int) or x < 0 for x in available):
        return "Available values must be non-negative whole numbers."
    if any(not isinstance(x, int) or x < 0 for row in allocation + maximum for x in row):
        return "Allocation and Max must contain non-negative whole numbers."
    for i in range(len(allocation)):
        for j in range(m):
            if allocation[i][j] > maximum[i][j]:
                return f"Invalid input: P{i} Allocation cannot exceed its Max for resource R{j}."
    return None

def safety_algorithm(available, allocation, need):
    work = available[:]
    finished = [False] * len(allocation)
    sequence, steps = [], []
    while len(sequence) < len(allocation):
        found = False
        for i in range(len(allocation)):
            if not finished[i] and all(need[i][j] <= work[j] for j in range(len(work))):
                before = work[:]
                released = allocation[i][:]
                work = [work[j] + released[j] for j in range(len(work))]
                finished[i] = True
                sequence.append(f"P{i}")
                steps.append({
                    "Process": f"P{i}",
                    "Need": str(need[i]),
                    "Work before": str(before),
                    "Allocation released": str(released),
                    "Work after": str(work)
                })
                found = True
                break
        if not found:
            break
    unfinished = [f"P{i}" for i, done in enumerate(finished) if not done]
    return len(sequence) == len(allocation), sequence, steps, unfinished

def request_check(pid, request, available, allocation, maximum):
    n, m = len(allocation), len(available)
    if pid < 0 or pid >= n:
        return "INVALID: process ID does not exist.", None, None
    if len(request) != m:
        return "INVALID: request must include one value for every resource type.", None, None
    if any(x < 0 for x in request):
        return "INVALID: resource requests cannot be negative.", None, None
    need = need_matrix(maximum, allocation)
    if any(request[j] > need[pid][j] for j in range(m)):
        return "INVALID: request exceeds this process's remaining Need.", None, None
    if any(request[j] > available[j] for j in range(m)):
        return "WAIT: request is valid but exceeds currently Available resources. State remains unchanged.", None, None
    temp_available = [available[j] - request[j] for j in range(m)]
    temp_allocation = deepcopy(allocation)
    temp_allocation[pid] = [temp_allocation[pid][j] + request[j] for j in range(m)]
    temp_need = need_matrix(maximum, temp_allocation)
    safe, seq, steps, unfinished = safety_algorithm(temp_available, temp_allocation, temp_need)
    simulation = {"available": temp_available, "allocation": temp_allocation, "need": temp_need,
                  "safe": safe, "sequence": seq, "steps": steps, "unfinished": unfinished}
    if safe:
        return "GRANTED in simulation: the resulting state is safe.", simulation, simulation
    return "DENIED: temporary allocation is unsafe. No complete safe sequence exists; original state is restored.", simulation, None

def show_matrix(title, rows, columns):
    frame = pd.DataFrame(rows, columns=columns, index=[f"P{i}" for i in range(len(rows))])
    frame.index.name = "Process"
    st.markdown(f"**{title}**")
    st.dataframe(frame, use_container_width=True)

def state_from_session():
    return (st.session_state.available, st.session_state.allocation, st.session_state.maximum)

if "available" not in st.session_state:
    st.session_state.available = DEFAULT_AVAILABLE[:]
    st.session_state.allocation = deepcopy(DEFAULT_ALLOCATION)
    st.session_state.maximum = deepcopy(DEFAULT_MAXIMUM)
if "last_request_result" not in st.session_state:
    st.session_state.last_request_result = None
if "request_simulation" not in st.session_state:
    st.session_state.request_simulation = None

with st.sidebar:
    st.header("Dashboard menu")
    page = st.radio("Go to section", [
        "Overview", "Scenario A — Safe State", "Scenario B — Exceeds Available",
        "Scenario C — Unsafe Request", "Scenario D — Deadlock Detection",
        "Scenario E — Deadlock Prevention", "Scenario F — Boundary Inputs",
        "Activity Test Report"
    ])
    st.divider()
    if st.button("Reset all to standard example", use_container_width=True):
        st.session_state.available = DEFAULT_AVAILABLE[:]
        st.session_state.allocation = deepcopy(DEFAULT_ALLOCATION)
        st.session_state.maximum = deepcopy(DEFAULT_MAXIMUM)
        st.session_state.last_request_result = None
        st.session_state.request_simulation = None
        st.rerun()
    st.caption("Standard example: 5 processes and 3 resource types.")

available, allocation, maximum = state_from_session()
err = validate_state(available, allocation, maximum)
resources = [f"R{j}" for j in range(len(available))]
need = need_matrix(maximum, allocation) if not err else []
safe, sequence, safety_steps, unfinished = safety_algorithm(available, allocation, need) if not err else (False, [], [], [])

if page == "Overview":
    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.subheader("Welcome")
        st.write("Use this dashboard to explore how an operating system allocates resources, avoids unsafe allocations, detects deadlocks, and prevents deadlock conditions.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Processes", len(allocation))
        c2.metric("Resource types", len(available))
        c3.metric("Current state", "SAFE" if safe else ("INVALID" if err else "UNSAFE"))
        st.markdown("### Deadlock in simple words")
        st.info("Deadlock happens when processes wait for resources held by one another, so none can continue. Example: P0 holds the printer and waits for the scanner, while P1 holds the scanner and waits for the printer.")
        st.markdown("### Four necessary conditions")
        st.markdown("""
        1. **Mutual exclusion:** a resource can be used by only one process at a time.
        2. **Hold and wait:** a process holds a resource while waiting for another.
        3. **No preemption:** resources cannot be forcibly taken under the current rules.
        4. **Circular wait:** processes form a waiting cycle.
        """)
        st.markdown("### Key difference")
        st.write("Banker’s Algorithm checks whether granting a request preserves a safe state. It does not, by itself, detect an existing deadlock. An unsafe state is not automatically a deadlock.")
    with right:
        st.subheader("▶ Live mini-simulation")
        st.caption("A small animated-style walkthrough of two processes waiting on each other.")
        sim_step = st.select_slider("Simulation step", options=[1, 2, 3], value=1,
                                    format_func=lambda x: {1:"1 · Resources held", 2:"2 · Both request", 3:"3 · Deadlock"}[x])
        if sim_step == 1:
            st.markdown('<div class="sim-card"><div class="sim-title">P0 holds 🖨️ Printer</div><div class="sim-sub">P1 holds 📄 Scanner</div></div>', unsafe_allow_html=True)
            st.success("Both processes currently hold one resource.")
        elif sim_step == 2:
            st.markdown('<div class="sim-card"><div class="sim-title">P0 → requests Scanner</div><div class="sim-sub">P1 → requests Printer</div></div>', unsafe_allow_html=True)
            st.warning("Each process is waiting for the resource held by the other.")
        else:
            st.markdown('<div class="sim-card"><div class="sim-title">P0 ⟲ P1</div><div class="sim-sub">Circular wait: neither process can continue.</div></div>', unsafe_allow_html=True)
            st.error("DEADLOCK under the assumption of one instance of each resource and no preemption.")
        st.markdown("**How to recover:** terminate one process and release its resources.")
        if st.button("Simulate recovery", use_container_width=True):
            st.session_state.recovered = True
        if st.session_state.get("recovered", False):
            st.success("P1 terminated → Scanner released → P0 can continue. Circular wait is broken.")
    st.divider()
    st.subheader("Assignment coverage")
    st.markdown("""
    - **A:** Need matrix, Work vector updates, safe sequence and safety explanation.
    - **B:** Valid request greater than Available; verify state is unchanged.
    - **C:** Temporary grant, safety test, deny unsafe request and restore state.
    - **D:** Resource relationships, circular wait, assumptions and recovery.
    - **E:** Apply prevention policy and explain trade-offs.
    - **F:** Zero resources, zero Need, invalid process IDs, negative requests and Allocation greater than Max.
    """)

elif page == "Scenario A — Safe State":
    st.subheader("Scenario A: Safe State")
    st.write("Configure Available, Allocation, and Max. The dashboard calculates Need = Max − Allocation and runs the safety algorithm.")
    n = st.number_input("Number of processes", min_value=1, max_value=8, value=len(allocation), step=1)
    m = st.number_input("Number of resource types", min_value=1, max_value=5, value=len(available), step=1)
    if n != len(allocation) or m != len(available):
        st.warning("Changing the matrix size creates zero-filled matrices when you click the button.")
        if st.button("Create matrices for selected size"):
            st.session_state.available = [0] * int(m)
            st.session_state.allocation = [[0] * int(m) for _ in range(int(n))]
            st.session_state.maximum = [[0] * int(m) for _ in range(int(n))]
            st.rerun()
    else:
        av_cols = st.columns(int(m))
        new_av = [av_cols[j].number_input(f"Available R{j}", min_value=0, max_value=999,
                                          value=int(available[j]), key=f"scenarioA_av_{j}") for j in range(int(m))]
        st.markdown("**Allocation matrix — edit the digits directly**")
        alloc_df = pd.DataFrame(allocation, columns=resources, index=[f"P{i}" for i in range(int(n))])
        alloc_df.index.name = "Process"
        edit_alloc = st.data_editor(alloc_df, key="scenarioA_alloc", use_container_width=True)
        st.markdown("**Maximum matrix — edit the digits directly**")
        max_df = pd.DataFrame(maximum, columns=resources, index=[f"P{i}" for i in range(int(n))])
        max_df.index.name = "Process"
        edit_max = st.data_editor(max_df, key="scenarioA_max", use_container_width=True)
        if st.button("Apply configuration", type="primary"):
            try:
                a = [[int(edit_alloc.iloc[i, j]) for j in range(int(m))] for i in range(int(n))]
                mx = [[int(edit_max.iloc[i, j]) for j in range(int(m))] for i in range(int(n))]
                av = [int(x) for x in new_av]
                e = validate_state(av, a, mx)
                if e:
                    st.error(e)
                else:
                    st.session_state.available, st.session_state.allocation, st.session_state.maximum = av, a, mx
                    st.rerun()
            except Exception:
                st.error("Use non-negative whole numbers only.")
    available, allocation, maximum = state_from_session()
    err = validate_state(available, allocation, maximum)
    if err:
        st.error(err)
    else:
        need = need_matrix(maximum, allocation)
        show_matrix("Need matrix (Max − Allocation)", need, resources)
        safe, sequence, steps, unfinished = safety_algorithm(available, allocation, need)
        st.markdown("### Safety algorithm")
        st.write(f"Initial **Work = {available}**")
        if safe:
            st.success("SAFE STATE · Safe sequence: " + " → ".join(sequence))
            st.write("Why safe? Every process can finish in this order. After each process finishes, its Allocation is released back to Work.")
        else:
            st.error("UNSAFE STATE · No complete safe sequence exists for this configuration.")
            st.write("Processes not able to finish in this pass:", ", ".join(unfinished))
        if steps:
            st.markdown("**Work vector update after each process completes**")
            st.dataframe(pd.DataFrame(steps), use_container_width=True)
        if not safe:
            st.warning("Unsafe does not automatically mean deadlocked. It means this safety check cannot guarantee that all processes can finish.")

elif page == "Scenario B — Exceeds Available":
    st.subheader("Scenario B: Request exceeds Available resources")
    st.write("The request must be within the process's remaining Need, but at least one requested resource is not currently available. The request waits and the state remains unchanged.")
    st.info("Try the standard example after setting Available to (1, 1, 1): P1 requests (1, 2, 2). This is within P1's Need (1, 2, 2), but exceeds the available scanners and tape drives.")
    st.markdown("### Set up a clear Scenario B test")
    if st.button("Load Scenario B example"):
        st.session_state.available = [1, 1, 1]
        st.session_state.allocation = deepcopy(DEFAULT_ALLOCATION)
        st.session_state.maximum = deepcopy(DEFAULT_MAXIMUM)
        st.session_state.last_request_result = None
        st.session_state.request_simulation = None
        st.rerun()
    available, allocation, maximum = state_from_session()
    need = need_matrix(maximum, allocation)
    show_matrix("Current Need matrix", need, [f"R{j}" for j in range(len(available))])
    st.write("Available:", available)
    pid = st.number_input("Process ID", min_value=0, max_value=max(0, len(allocation)-1), value=1, step=1)
    request = [st.number_input(f"Request R{j}", min_value=-99, max_value=999, value=[1,2,2][j] if j < 3 else 0, key=f"scenarioB_req_{j}") for j in range(len(available))]
    before = {"Available": available[:], "Allocation": deepcopy(allocation)}
    if st.button("Check Scenario B request", type="primary"):
        result, simulation, accepted = request_check(int(pid), request, available, allocation, maximum)
        st.session_state.last_request_result = result
        st.session_state.request_simulation = simulation
        st.session_state.request_before = before
    if st.session_state.last_request_result:
        result = st.session_state.last_request_result
        if result.startswith("WAIT"):
            st.warning(result)
            st.markdown("**Verification — state unchanged**")
            st.write("Available before:", st.session_state.request_before["Available"])
            st.write("Available after:", st.session_state.available)
            st.write("Allocation unchanged:", st.session_state.request_before["Allocation"] == st.session_state.allocation)
        elif result.startswith("GRANTED"):
            st.success(result)
        else:
            st.error(result)

elif page == "Scenario C — Unsafe Request":
    st.subheader("Scenario C: Request would produce an unsafe state")
    st.write("This test uses the standard example and requests (3, 3, 0) from P4. The request is within P4's Need and Available, but granting it would leave no complete safe sequence.")
    if st.button("Load Scenario C example"):
        st.session_state.available = DEFAULT_AVAILABLE[:]
        st.session_state.allocation = deepcopy(DEFAULT_ALLOCATION)
        st.session_state.maximum = deepcopy(DEFAULT_MAXIMUM)
        st.session_state.last_request_result = None
        st.session_state.request_simulation = None
        st.rerun()
    available, allocation, maximum = state_from_session()
    need = need_matrix(maximum, allocation)
    show_matrix("Current Need matrix", need, [f"R{j}" for j in range(len(available))])
    pid = st.number_input("Process ID (P4 = 4)", min_value=0, max_value=max(0, len(allocation)-1), value=min(4, len(allocation)-1), step=1)
    default_req = [3,3,0]
    request = [st.number_input(f"Request R{j}", min_value=-99, max_value=999,
                               value=default_req[j] if j < 3 else 0, key=f"scenarioC_req_{j}") for j in range(len(available))]
    if st.button("Temporarily grant and run safety check", type="primary"):
        before = {"available": available[:], "allocation": deepcopy(allocation), "need": deepcopy(need)}
        result, simulation, accepted = request_check(int(pid), request, available, allocation, maximum)
        st.session_state.last_request_result = result
        st.session_state.request_simulation = simulation
        st.session_state.request_before_C = before
    if st.session_state.last_request_result:
        result = st.session_state.last_request_result
        simulation = st.session_state.request_simulation
        if simulation:
            st.markdown("### Temporary simulated allocation")
            st.write("Temporary Available:", simulation["available"])
            show_matrix("Temporary Allocation", simulation["allocation"], [f"R{j}" for j in range(len(available))])
            show_matrix("Temporary Need", simulation["need"], [f"R{j}" for j in range(len(available))])
            if simulation["safe"]:
                st.success("Temporary state is safe. " + " → ".join(simulation["sequence"]))
            else:
                st.error("No complete safe sequence. Unfinished processes: " + ", ".join(simulation["unfinished"]))
        if result.startswith("DENIED"):
            st.error(result)
            st.write("Original Available restored:", available)
            st.write("Original Allocation restored:", allocation)
            st.info("Unsafe does not necessarily mean deadlocked. It means the system cannot guarantee completion for every process.")
        elif result.startswith("GRANTED"):
            st.success(result)
        else:
            st.warning(result)

elif page == "Scenario D — Deadlock Detection":
    st.subheader("Scenario D: Deadlock detection")
    st.write("Separate example: one instance of Printer and one instance of Scanner, with no forced resource preemption.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Resource allocation")
        st.markdown("- Printer → P0 (P0 holds Printer)\n- Scanner → P1 (P1 holds Scanner)")
    with col2:
        st.markdown("### Outstanding requests")
        st.markdown("- P0 → Scanner (waits for Scanner held by P1)\n- P1 → Printer (waits for Printer held by P0)")
    st.graphviz_chart("""
    digraph {
      rankdir=LR;
      P0 [shape=box, style=filled, fillcolor="#dbeafe"];
      P1 [shape=box, style=filled, fillcolor="#fce7f3"];
      Printer [shape=ellipse];
      Scanner [shape=ellipse];
      Printer -> P0 [label="allocated"];
      Scanner -> P1 [label="allocated"];
      P0 -> Scanner [label="requests", color="red"];
      P1 -> Printer [label="requests", color="red"];
    }
    """)
    st.error("Confirmed deadlock under these assumptions: each resource has one instance and the processes cannot be forced to release resources.")
    st.warning("A cycle alone may only indicate a potential deadlock when resource types have multiple instances. State the resource-instance assumptions.")
    if "recovery_done" not in st.session_state:
        st.session_state.recovery_done = False
    if st.button("Recover: terminate P1 and release Scanner"):
        st.session_state.recovery_done = True
    if st.session_state.recovery_done:
        st.success("P1 is terminated → Scanner is released → P0 obtains Scanner and can finish. The cycle is broken.")
        st.write("Trade-off: terminating P1 may lose its unfinished work.")

elif page == "Scenario E — Deadlock Prevention":
    st.subheader("Scenario E: Deadlock prevention")
    policy = st.radio("Choose a prevention policy", [
        "Fixed resource acquisition order (prevents circular wait)",
        "Request all needed resources before execution (prevents hold and wait)"
    ])
    st.markdown("### Original situation")
    st.write("P0 holds Printer and waits for Scanner. P1 holds Scanner and waits for Printer. Circular wait can occur.")
    st.markdown("### Modified policy")
    if policy.startswith("Fixed"):
        st.write("Set a global order: 1 = Printer, 2 = Scanner. Every process must request Printer before Scanner. A process must never hold Scanner and then request Printer.")
        st.success("Circular wait is prevented by the fixed order.")
        st.markdown("**Trade-off:** Processes may wait longer if the first resource is unavailable.")
    else:
        st.write("A process requests all resources it needs before it starts. If all resources are not available, it waits without holding any of them.")
        st.success("Hold and wait is prevented.")
        st.markdown("**Trade-off:** Resources may remain unused while reserved, reducing utilization and concurrency.")
    st.markdown("### Comparison")
    st.dataframe(pd.DataFrame([
        {"Policy": "Original", "Deadlock risk": "Circular wait can occur", "Resource use": "May be more flexible"},
        {"Policy": "Modified", "Deadlock risk": "Selected condition prevented", "Resource use": "May wait longer or reduce concurrency"}
    ]), use_container_width=True)

elif page == "Scenario F — Boundary Inputs":
    st.subheader("Scenario F: Boundary and invalid inputs")
    st.write("Use the interactive tests below. Valid boundary states should not be confused with invalid inputs.")
    with st.expander("Test zero Available resources"):
        zero_av = [0] * len(available)
        st.write("Available =", zero_av)
        zero_need = [[0] * len(available) for _ in allocation]
        can_finish = [i for i, row in enumerate(zero_need) if all(x == 0 for x in row)]
        st.write("With zero Available, a process can still finish immediately if its remaining Need is all zero.")
        st.write("Processes with zero Need in this illustrative check:", can_finish if can_finish else "None in this example.")
    with st.expander("Test process with zero remaining Need"):
        idx = st.selectbox("Choose process", list(range(len(allocation))), format_func=lambda x: f"P{x}")
        this_need = need_matrix(maximum, allocation)[idx]
        st.write(f"Need for P{idx} =", this_need)
        if all(x == 0 for x in this_need):
            st.success("This process can finish immediately and release its Allocation.")
        else:
            st.info("This process does not have zero Need in the current state. Edit Max to match Allocation to create this boundary case.")
    with st.expander("Test invalid process identifier"):
        bad_pid = st.number_input("Enter process ID", min_value=0, max_value=999, value=99, step=1)
        if st.button("Validate process ID"):
            if bad_pid >= len(allocation):
                st.error("Invalid process ID: this process does not exist.")
            else:
                st.success("Process ID is valid.")
    with st.expander("Test negative request"):
        neg = st.number_input("Request value", min_value=-999, max_value=999, value=-1, step=1)
        if st.button("Validate negative request"):
            if neg < 0:
                st.error("Invalid request: resource counts cannot be negative.")
            else:
                st.success("Request value is non-negative.")
    with st.expander("Test Allocation exceeding Max"):
        p = st.number_input("Process to test", min_value=0, max_value=max(0, len(allocation)-1), value=0, step=1)
        r = st.number_input("Resource index to test", min_value=0, max_value=max(0, len(available)-1), value=0, step=1)
        if st.button("Create invalid Allocation test"):
            invalid_alloc = deepcopy(allocation)
            invalid_alloc[int(p)][int(r)] = maximum[int(p)][int(r)] + 1
            validation = validate_state(available, invalid_alloc, maximum)
            st.error(validation or "Invalid input was not detected.")
    st.markdown("### Validation rules")
    st.markdown("- Zero Available is a valid boundary case.\n- Zero remaining Need is valid; that process can finish and release resources.\n- Invalid process IDs and negative requests must be rejected.\n- Allocation greater than Max must be rejected.\n- A request greater than Available but within Need must wait, not be labelled invalid.")

elif page == "Activity Test Report":
    st.subheader("Activity Test Report — TC1 to TC6")
    st.caption("Use this table as a report guide. Replace/confirm the actual result after running each scenario.")
    report = [
        {"Test": "TC1", "Condition": "Safe state", "Expected result": "Safe sequence found", "Analysis": "All processes can finish in the displayed order."},
        {"Test": "TC2", "Condition": "Request exceeds Available", "Expected result": "Wait; state unchanged", "Analysis": "Request is within Need but resources are not currently available."},
        {"Test": "TC3", "Condition": "Request makes state unsafe", "Expected result": "Denied; state restored", "Analysis": "Temporary allocation has no complete safe sequence."},
        {"Test": "TC4", "Condition": "Deadlocked scenario", "Expected result": "Deadlock identified", "Analysis": "Circular wait under stated single-instance assumptions; show recovery."},
        {"Test": "TC5", "Condition": "Prevention policy applied", "Expected result": "One condition eliminated", "Analysis": "Fixed ordering prevents circular wait or all-at-once requests prevent hold and wait."},
        {"Test": "TC6", "Condition": "Boundary and invalid inputs", "Expected result": "Correct handling/message", "Analysis": "Separate valid boundary cases from invalid values."},
    ]
    st.dataframe(pd.DataFrame(report), use_container_width=True, hide_index=True)
    csv = pd.DataFrame(report).to_csv(index=False).encode("utf-8")
    st.download_button("Download test report CSV", data=csv, file_name="activity_test_report.csv", mime="text/csv")

st.divider()
st.caption("Educational demonstration. Verify actual outputs and explain the algorithm during your viva.")
