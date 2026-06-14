# **Moving Helper AI 搬家助手**

## 1. Project Overview 项目简介


Moving Helper AI is a multimodal moving assistant that helps users organize and plan a move using voice, images, live video, and text inputs.

The goal is to reduce the effort required to estimate moving needs, identify moving items, and generate personalized moving recommendations.


Moving Helper AI 是一个多模态搬家助手，用户可以通过语音、图片、实时视频和文本输入来规划搬家流程。

项目目标是帮助用户更轻松地整理搬家需求、识别需要搬运的物品，并生成个性化的搬家建议。



## 2. Planned User Stories 用户故事

### User Story 1



As a user, I want to describe my moving situation using voice so that I do not need to manually type everything and can save time.



作为用户，我希望能够通过语音描述自己的搬家需求，而不需要手动输入大量信息，从而节省时间。

Status / 状态：Implemented 已实现



### User Story 2



As a user, I want to upload photos of my room so that AI can understand what items I need to move.



作为用户，我希望上传房间照片，让 AI 能够了解我需要搬运哪些物品。

Status / 状态：Implemented 已实现



### User Story 3



As a user, I want to use my webcam to show my belongings so that AI can analyze the current environment.



作为用户，我希望使用摄像头展示当前环境和物品，让 AI 能够进行分析。

Status / 状态：Implemented 已实现



### User Story 4



As a user, I want AI to automatically extract moving information such as move date, budget, storage needs, and transportation requirements.

To achieve this, I designed prompts that allow AI to automatically analyze and extract structured information from voice transcripts.



作为用户，我希望 AI 能够自动提取搬家日期、预算、仓储需求以及运输需求等信息。

为此，我设计了专门的 Prompt，使 AI 能够从语音转写结果中自动提取结构化信息。

Status / 状态：Implemented 已实现



### User Story 5



As a user, I want AI to generate a complete moving plan including packing suggestions, storage advice, and moving timelines.



作为用户，我希望 AI 能够生成完整的搬家计划，包括打包建议、仓储建议以及时间安排。

Status / 状态：Implemented 已实现



## 3. System Architecture 系统架构

Input Layer 输入层

* Voice Input 语音输入
* Image Upload 图片上传
* Live Video 实时视频
* Text Input 文本输入

↓

Processing Layer 处理层

* Whisper Speech Recognition 语音识别
* GPT-4.1 Mini Information Extraction 信息提取
* Image Analysis 图像分析

↓

Output Layer 输出层

* Moving Recommendations 搬家建议
* Packing Suggestions 打包建议
* Storage Planning 仓储规划
* Moving Timeline 时间安排



## 4. Cost Optimization Ideas 成本优化思路

Ideas Considered 曾考虑的方案

* Real-time video analysis 实时视频分析
* Continuous video streaming 持续视频流处理
* Large reasoning models 大型推理模型
* Full video processing 完整视频处理

Problems 存在的问题

These approaches significantly increase API costs and computational requirements.

这些方案会显著增加 API 调用成本和计算资源消耗。



## 5. Cost Optimization Techniques Actually Used 实际采用的成本优化策略

### Technique 1 策略一

Use GPT-4.1 Mini instead of larger models.

使用 GPT-4.1 Mini 替代更大的模型。

Benefit / 优势

Lower API cost while maintaining acceptable quality.

在保证结果质量的前提下降低 API 成本。



### Technique 2 策略二

Use Whisper transcription once and store the result in session state.

语音仅转写一次，并将结果存储在 Session State 中。

Benefit / 优势

Avoid repeated speech-to-text requests.

避免重复调用语音识别接口。



### Technique 3 策略三

Process only uploaded images and optional video frames.

仅处理用户主动上传的图片和选定的视频帧。

Benefit / 优势

Avoid continuous video processing costs.

避免持续视频分析带来的高额成本。



### Technique 4 策略四

Reuse extracted moving information.

重复利用已经提取出的结构化信息。

Benefit / 优势

Reduce duplicate API calls.

减少重复的 API 请求。



## 6. Future Improvements 未来改进方向

* Moving cost estimation 搬家费用估算
* Truck size recommendation 搬家车辆推荐
* Storage size recommendation 仓储空间推荐
* Integration with moving companies 对接搬家公司服务
* Real-time video analysis 实时视频分析
* Mobile deployment 移动端部署



## 7. Conclusion 总结



Moving Helper AI demonstrates how multimodal AI can simplify moving-related planning tasks while maintaining low operational cost through selective processing and lightweight model choices.



Moving Helper AI 展示了多模态 AI 如何帮助用户简化搬家规划流程，并通过轻量级模型和选择性处理策略有效控制运营成本。
