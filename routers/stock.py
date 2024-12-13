from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

router = APIRouter()

@router.get("/quote/{symbol}")
async def get_stock_quote(symbol: str) -> Dict[str, Any]:
    """获取股票实时报价"""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol,
            "name": info.get("longName", ""),
            "price": info.get("currentPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "changePercent": info.get("regularMarketChangePercent", 0),
            "volume": info.get("regularMarketVolume", 0),
            "marketCap": info.get("marketCap", 0),
            "high": info.get("regularMarketDayHigh", 0),
            "low": info.get("regularMarketDayLow", 0),
            "open": info.get("regularMarketOpen", 0),
            "previousClose": info.get("regularMarketPreviousClose", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获���股票数据失败: {str(e)}")

@router.get("/history/{symbol}")
async def get_stock_history(
    symbol: str, 
    period: str = "1mo",  # 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    interval: str = "1d"  # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
) -> List[Dict[str, Any]]:
    """获取股票历史数据"""
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval)
        
        return [{
            "date": index.strftime('%Y-%m-%d %H:%M:%S'),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"]
        } for index, row in history.iterrows()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取历史数据失败: {str(e)}")

@router.get("/indicators/{symbol}")
async def get_technical_indicators(symbol: str) -> Dict[str, Any]:
    """获取技术指标"""
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo")
        
        # 计算移动平均线
        ma5 = history["Close"].rolling(window=5).mean().iloc[-1]
        ma10 = history["Close"].rolling(window=10).mean().iloc[-1]
        ma20 = history["Close"].rolling(window=20).mean().iloc[-1]
        
        # 计算RSI
        delta = history["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        return {
            "symbol": symbol,
            "ma5": ma5,
            "ma10": ma10,
            "ma20": ma20,
            "rsi": rsi,
            "volume_ma5": history["Volume"].rolling(window=5).mean().iloc[-1],
            "last_price": history["Close"].iloc[-1],
            "price_change": history["Close"].iloc[-1] - history["Close"].iloc[-2],
            "price_change_percent": (history["Close"].iloc[-1] / history["Close"].iloc[-2] - 1) * 100
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"获取技术指标失败: {str(e)}")

@router.get("/search")
async def search_stocks(query: str) -> List[Dict[str, Any]]:
    """搜索股票"""
    try:
        tickers = yf.Tickers(query)
        results = []
        for symbol in query.split():
            try:
                info = tickers.tickers[symbol].info
                results.append({
                    "symbol": symbol,
                    "name": info.get("longName", ""),
                    "exchange": info.get("exchange", ""),
                    "industry": info.get("industry", ""),
                    "sector": info.get("sector", "")
                })
            except:
                continue
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"搜索失败: {str(e)}") 