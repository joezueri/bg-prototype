import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import streamlit.components.v1 as components
from database import get_connection
from init import create_table

create_table()  # run once to ensure table exists

st.title("Hello Streamlit Cloud!")
st.write("This is my first deployed app 🚀")

components.html(
    """
    <button onclick="sendValue()">Send 42 to Backend</button>
    <script>
        function sendValue() {
            const currentUrl = window.parent.location.href.split('?')[0];
            const newUrl = currentUrl + "?value=42";
            window.parent.location.href = newUrl;
        }
    </script>
    <script>
      alert("JS loaded!");
    </script>
    """,
    height=100,
)

# Use query_params to read the value
value = st.query_params.get("value")

if value:
    st.success(f"Received from JavaScript: {value}")
else:
    st.info("Click the button to send value 42.")


name = st.text_input("Name")

if st.button("Add project"):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO projecttable (name) VALUES (?)"
    params = (name,)  # Note the comma to make it a tuple

    st.text(sql) 
    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    st.success("Project added!")

# Display users
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM projecttable")
rows = cursor.fetchall()


for row in rows:
    id_, name = row
    cols = st.columns([1, 4, 1])
    cols[0].write(id_)
    cols[1].write(name)
    if cols[2].button('❌delete', key=f'del_{id_}'):
        cursor.execute("DELETE FROM projecttable WHERE id = ?", (id_,))
        conn.commit()
        st.success(f"Deleted project ID {id_}")
        st.rerun()
conn.close()
#st.write(rows)

# Catch the postMessage in Streamlit via JS Eval
result = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve) => {
      console.log("📡 JS Listener: Setting up message listener...");
      window.addEventListener('message', (event) => {
        console.log("📨 Message received:", event);
        if (event.data?.type === 'mindmap_data') {
          console.log("✅ Mind map data received in JS:", event.data.data);
          resolve(event.data.data);
        }
      });
    })
    """,
    key="get_mindmap_data"
)

result = streamlit_js_eval(
    js_expressions="""
    new Promise((resolve) => {
      console.log("📡 Setting up JS message listener");
      window.addEventListener('message', (event) => {
        console.log("📨 Received message in JS:", event);
        if (event.data?.type === 'mindmap_data') {
          console.log("✅ Mind map data received in JS:", event.data.data);
          resolve(event.data.data);
        }
      });
    })
    """,
    key="debug_message"
)


# Show result
if result:
    st.write("📥 `result` object received.")
    if result.value:
        st.success("✅ Mind map data received!")
        st.json(result.value)
    else:
        st.warning("❗ Result received but `.value` is empty.")
else:
    st.warning("⛔ No result object yet.")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>jsMind in Streamlit</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jsmind@0.4.6/style/jsmind.css" />
  <script src="https://cdn.jsdelivr.net/npm/jsmind@0.4.6/js/jsmind.js"></script>
  <style>
    #jsmind_container {
      width: 100%;
      height: 400px;
      border: solid 1px #ccc;
      background: #f4f4f4;
    }
    .controls {
      margin-top: 10px;
    }
    .controls button {
      margin-right: 10px;
      padding: 8px 12px;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div id="jsmind_container"></div>
  <div class="controls">
    <button onclick="addNode()">➕ Add Node</button>
    <button onclick="addToRoot()">➕ Add to Root</button>
    <button onclick="saveMindMap()">💾 Save Mind Map</button>
  </div>

  <script>
    window.onload = function() {
      var mind = {
        "meta": {
          "name": "demo",
          "author": "xy",
          "version": "1.0"
        },
        "format": "node_array",
        "data": [
          {"id": "root", "isroot": true, "topic": "Main Topic"},
          {"id": "sub1", "parentid": "root", "topic": "Sub Node 1"},
          {"id": "sub2", "parentid": "root", "topic": "Sub Node 2"}
        ]
      };

      var options = {
        container: 'jsmind_container',
        editable: true,
        theme: 'primary'
      };

      window.jm = jsMind.show(options, mind);
    }

    function addNode() {
      const selected = window.jm.get_selected_node();
      if (!selected) {
        alert("Please select a node first.");
        return;
      }
      const newId = 'node_' + Date.now();
      window.jm.add_node(selected, newId, 'New Node');
    }

    function addToRoot() {
      const selected = window.jm.get_selected_node();
      const root = window.jm.get_root();
      const target = selected || root;
      const newId = 'node_' + Date.now();
      window.jm.add_node(target, newId, 'New Node');
    }
    function saveMindMap() {
      const mindData = window.jm.get_data();
      // Send the data to Streamlit
      //window.parent.postMessage({ type: 'mindmap_data', data: JSON.stringify(mindData) }, '*');
      //window.parent.postMessage({ type: 'mindmap_data', data: mindData }, '*');
      window.postMessage({ type: 'mindmap_data', data: mindData }, '*');
    }
  </script>
</body>
</html>
"""

components.html(html_code, height=500)

