## Verlet Integration
**Create, edit and simulate physical objects in python.**<br>


### rag.py
Data and functions for ragdoll objects (contains all functions for verlet integration)
<br>
### editor.py 
gui editor for .rag (json) files<br>
**controls**:
- left click to place points in "point mode"
- right click on points in "point mode" to toggle the point's static property
- left click on a point and drag to another point to connect them with in "stick mode"

### main.py
loads object.rag file and runs physics simulation<br>
**controls**:
- use buttons to change properties<br>
- click and drag on the points to move them
