# Usage

```python
from fastapi import FastAPI
from fastapi_admin_lite import add_admin

app = FastAPI()
add_admin(app, db_url="sqlite:///admin.db")

# Access admin at /admin
```