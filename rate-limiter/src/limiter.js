const Redis = require("ioredis");
const redis = new Redis();

async function tokenBucketLimit(userId, limit = 10, window = 60) {
    const key = `limiter:${userId}`;
    const current = await redis.get(key);
    
    if (current && parseInt(current) >= limit) {
        return { allowed: false, remaining: 0 };
    }
    
    const newValue = await redis.incr(key);
    if (newValue === 1) await redis.expire(key, window);
    
    return { allowed: true, remaining: limit - newValue };
}

module.exports = { tokenBucketLimit };
