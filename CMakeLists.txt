cmake_minimum_required(VERSION 3.5)
project(WxFunny)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
        Spider/main.py
        Spider/spider_config.py
        Spider/spider_sina.py
        Spider/spider_tool.py
        Spider/spider_url.py)

add_executable(WxFunny ${SOURCE_FILES})