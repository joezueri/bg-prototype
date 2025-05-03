import streamlit as st

st.set_page_config(page_title="Mind Map with jsMind")

st.title("Mind Map Demo with jsMind")

import streamlit.components.v1 as components

html_code = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/jsmind@0.4.6/js/jsmind.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jsmind@0.4.6/style/jsmind.css" />
</head>
<body>
  <div id="jsmind_container" style="width:100%; height:400px; border: 1px solid #ccc; margin-bottom: 10px;"></div>
  <button onclick="addNode()">➕ Add Node</button>
  <button onclick="saveMindMap()">💾 Save Mind Map</button>

  <script>
    const mind = {
      meta: { name: "demo", author: "you", version: "1.0" },
      format: "node_array",
      data: [
        { id: "root", isroot: true, topic: "Central Topic" },
        { id: "sub1", parentid: "root", topic: "Idea 1" },
        { id: "sub2", parentid: "root", topic: "Idea 2" }
      ]
    };

    const options = {
      container: 'jsmind_container',
      editable: true,
      theme: 'primary'
    };

    const jm = jsMind.show(options, mind);

    function addNode() {
      const selected = jm.get_selected_node();
      if (!selected) {
        alert("Please select a node first.");
        return;
      }
      const newId = 'node_' + Date.now();
      jm.add_node(selected, newId, 'New Node');
    }

    function saveMindMap() {
      const mindData = jm.get_data(); // Gets the full mind map
      alert("Mind Map JSON:\n" + JSON.stringify(mindData, null, 2));
    }
  </script>
</body>
</html>

"""

components.html(html_code, height=450)