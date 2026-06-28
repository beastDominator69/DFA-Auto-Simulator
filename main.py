from flask import Flask, render_template, request
import json

app = Flask(__name__)


def build_dfa_from_string(input_string):
    n = len(input_string)
    states = [f"q{i}" for i in range(n + 1)] + ["qDead"]
    alphabet = sorted(set(input_string))
    start = "q0"
    finals = [f"q{n}"]

    transitions = {}
    for i, ch in enumerate(input_string):
        state = f"q{i}"
        transitions[state] = {}
        transitions[state][ch] = f"q{i+1}"
        for sym in alphabet:
            if sym != ch:
                transitions[state][sym] = "qDead"

    transitions[f"q{n}"] = {sym: "qDead" for sym in alphabet}
    transitions["qDead"] = {sym: "qDead" for sym in alphabet}

    return states, alphabet, start, finals, transitions


def simulate_dfa(states, alphabet, start, finals, transitions, input_string):
    current = start
    trace = [f"Start: {current}"]

    if input_string == "":
        trace.append("Empty input string")
        trace.append(f"Final State: {current}")
        return ("ACCEPTED" if current in finals else "REJECTED"), trace

    for ch in input_string:
        if not ch.isalnum():
            return f"ERROR: Symbol '{ch}' not allowed", []

        if ch not in alphabet:
            # goes to dead
            trace.append(f"delta({current}, '{ch}') → qDead")
            current = "qDead"
            break

        if current not in transitions or ch not in transitions[current]:
            return f"ERROR: Missing transition for ({current}, {ch})", []

        next_state = transitions[current][ch]
        trace.append(f"delta({current}, '{ch}') → {next_state}")
        current = next_state

    trace.append(f"Final State: {current}")
    return ("ACCEPTED" if current in finals else "REJECTED"), trace


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    trace = []
    graph_data = None
    input_string = ""
    test_string = ""
    dfa_info = None

    if request.method == "POST":
        input_string = request.form.get("input_string", "").strip()
        test_string  = request.form.get("test_string", "").strip()

        if not input_string:
            return render_template("index.html",
                                   result="ERROR: Please enter a target string.",
                                   trace=[], graph=None, dfa_info=None,
                                   input_string="", test_string="")

        if not all(c.isalnum() for c in input_string):
            return render_template("index.html",
                                   result="ERROR: Only letters and digits allowed.",
                                   trace=[], graph=None, dfa_info=None,
                                   input_string=input_string, test_string=test_string)

        states, alphabet, start, finals, transitions = build_dfa_from_string(input_string)

        dfa_info = {
            "states":   ", ".join(states),
            "alphabet": ", ".join(alphabet),
            "start":    start,
            "finals":   ", ".join(finals),
            "target":   input_string
        }

        sim_string = test_string if test_string else input_string

        # Build active path for highlighting
        active_edges = []
        current = start
        for ch in sim_string:
            if ch in transitions.get(current, {}):
                next_state = transitions[current][ch]
                active_edges.append(f"{current}|{ch}|{next_state}")
                current = next_state
            else:
                active_edges.append(f"{current}|{ch}|qDead")
                break

        result, trace = simulate_dfa(states, alphabet, start, finals, transitions, sim_string)

        # Build graph data for JS rendering
        nodes = []
        for s in states:
            nodes.append({
                "id":    s,
                "final": s in finals,
                "dead":  s == "qDead",
                "start": s == start
            })

        edges = []
        for state in transitions:
            # group symbols going to same target
            grouped = {}
            for sym, nxt in transitions[state].items():
                grouped.setdefault(nxt, []).append(sym)
            for nxt, syms in grouped.items():
                edges.append({
                    "from":   state,
                    "to":     nxt,
                    "label":  ",".join(sorted(syms)),
                    "active": any(f"{state}|{s}|{nxt}" in active_edges for s in syms)
                })

        graph_data = json.dumps({"nodes": nodes, "edges": edges})

    return render_template("index.html",
                           result=result,
                           trace=trace,
                           graph=graph_data,
                           dfa_info=dfa_info,
                           input_string=input_string,
                           test_string=test_string)


if __name__ == "__main__":
    app.run(debug=True)