# 07 | AKShare 数据获取 + SQLite 持久化

#python #akshare #sqlite #数据工程

## 6 种数据源速查

| 数据 | 函数 | 返回 | 注意事项 |
|------|------|------|---------|
| 个股日线 | `stock_zh_a_hist` | OHLCV + 涨跌幅 | 需要 `adjust` 参数 |
| 指数日线 | `stock_zh_index_daily_em` | 指数行情 | 代码格式 `sh000300` |
| 行业板块 | `stock_board_industry_hist_em` | 行业日线 | 传中文名如 `'半导体'` |
| 资金流向 | `stock_individual_fund_flow` | 主力/散户净流入 | 需要 `market='sh'/'sz'` |
| 龙虎榜 | `stock_sina_lhb_detail_daily` | 上榜明细 | 非交易日可能无数据 |
| 全市场快照 | `stock_zh_a_spot_em` | 5000+只实时 | 数据量大，日终调用一次 |

---

## SQLite 工具函数（完整版）

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 列名访问
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def save_to_sqlite(df, table_name, db_path='data.db', if_exists='replace'):
    with get_db(db_path) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    return len(df)

def read_from_sqlite(table_name, condition=None, db_path='data.db'):
    query = f"SELECT * FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    with get_db(db_path) as conn:
        return pd.read_sql_query(query, conn)

def list_tables(db_path='data.db'):
    with get_db(db_path) as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row['name'] for row in cur.fetchall()]
```

---

## 数据获取函数封装模式

```python
def get_stock_daily(symbol, start_date, end_date, adjust='qfq'):
    """标准化封装：中文列名→英文，加 symbol 列"""
    df = ak.stock_zh_a_hist(
        symbol=symbol, period='daily',
        start_date=start_date, end_date=end_date, adjust=adjust
    )
    df['symbol'] = symbol
    df = df.rename(columns={
        '日期': 'date', '开盘': 'open', '收盘': 'close',
        '最高': 'high', '最低': 'low', '成交量': 'volume',
        '涨跌幅': 'pct_change', '换手率': 'turnover'
    })
    df['date'] = pd.to_datetime(df['date'])
    return df
```

**封装的好处**：
- 复用：一个函数多处调用
- 容错：统一的错误处理
- 标准化：列名一致，后续代码不用适配

---

## 批量拉取 + 写入模式

```python
results = []
stocks = {'000001': '平安银行', '600519': '贵州茅台'}

for code, name in stocks.items():
    try:
        df = get_stock_daily(code, '20260101', '20260531')
        df['name'] = name
        n = save_to_sqlite(df, f'stock_{code}')
        results.append((name, n))
    except Exception as e:
        print(f'✗ {name}: {e}')
```

---

## 网络问题处理

AKShare 底层调用东方财富/新浪接口，常见问题：

```python
# ProxyError：本机代理不可达
# 解决：临时关闭代理
import os
saved = {}
for k in ['HTTP_PROXY', 'HTTPS_PROXY']:
    if k in os.environ:
        saved[k] = os.environ.pop(k)
# ... 调用 akshare ...
os.environ.update(saved)  # 恢复
```

```python
# 重试机制
for attempt in range(3):
    try:
        df = ak.stock_zh_a_hist(...)
        break
    except Exception:
        time.sleep(2 ** attempt)  # 指数退避
```

---

## 踩坑记录

| 坑 | 说明 |
|----|------|
| 列名是中文 | AKShare 返回中文列名，必须 rename |
| `to_sql` 默认不覆盖 | 用 `if_exists='replace'` |
| 数据量大时 | 全市场快照 5000+ 行，SQLite 写入要几秒 |
| 接口不稳定 | 加 try/except + 重试，别让整个 batch 挂掉 |
| 龙虎榜非交易日 | 会报错，用 try/except 包裹 |

---

📁 对应 Notebook: `07_akshare_sqlite_etl.ipynb`
⬅️ [[06-Pandas数据清洗]] ➡️ [[08-Matplotlib金融可视化]]

---

## 顺序通关导航

- 上一课：[[06-Pandas数据清洗]]
- 下一课：[[08-Matplotlib金融可视化]]
- 对应 Notebook：`07_akshare_sqlite_etl.ipynb`

## 本课复习检查点

- [ ] 我能用自己的话解释本课核心概念。
- [ ] 我能从上到下运行对应 Notebook。
- [ ] 我能改一个参数或场景，并解释结果变化。
