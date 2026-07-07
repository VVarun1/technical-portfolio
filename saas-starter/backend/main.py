from fastapi import FastAPI, Request
app = FastAPI()

@app.get("/api/data")
async def get_data(request: Request):
    tenant_id = request.headers.get("X-Tenant-ID")
    # Filter all DB queries by tenant_id for data isolation
    return {"data": f"Tenant {tenant_id} scoped data"}
