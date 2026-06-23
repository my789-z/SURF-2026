# Task 1: Run the Full Model and Prepare Ablation Studies

第一阶段目标是先理解并跑通当前完整模型，然后在相同代码风格下准备三个消融研究 notebook。请把每一步的代码、结果和说明都用 GitHub 记录下来。

## 1. Read and Run the Current Full Model

请先阅读并运行当前文件：

```text
notebook_full_model.ipynb
```

这个 notebook 的主线任务是：给定渗透率场，训练神经算子模型来预测 mixed GMsFEM 中的一个多尺度基函数。

第一次运行时请保持：

```python
RUN_MODE = "quick"
```

确认环境、数据读取、训练、保存和可视化都能正常运行后，再改成：

```python
RUN_MODE = "full"
```

正式训练完整模型。

## 2. Save the Full Model Results

请至少保存并检查以下内容：

- 训练好的模型 checkpoint，例如 `best_model/basis_04_best.pt`
- 训练历史文件，例如 `history_basis_04.mat`
- 测试指标表格，例如 `metrics_basis_04.csv`
- 预测结果数组，例如 `predictions_basis_04.npz`
- 运行配置与指标摘要，例如 `summary_basis_04.json`
- 可视化图片，例如预测结果、真实值和误差图

请在自己的实验记录中说明：

- 你训练的是第几个 basis function
- 使用的是 `quick` 还是 `full`
- 训练集、验证集、测试集大小
- epoch 数量
- 最终测试误差和 R2 指标
- 保存文件所在路径

## 3. Advanced Option: Predict All Basis Functions

基础任务只要求训练一个指定的基函数。

如果你已经成功跑通单个基函数，可以进一步尝试一次性或批量训练所有基函数。当前 notebook 最后的 advanced section 已经保留了批量训练所有 basis functions 的入口。

请注意：训练所有基函数会明显增加运行时间和显存/存储需求。建议先确认单个 basis function 的完整流程没有问题，再进行这个进阶实验。

## 4. Prepare Three Ablation Study Files

在完整模型跑通以后，请仿照 `notebook_full_model.ipynb` 的结构和说明风格，创建三个消融研究 notebook。文件名请使用：

```text
notebook_ablation_no_fno.ipynb
notebook_ablation_no_attention.ipynb
notebook_ablation_no_gradient_loss.ipynb
```

三个消融实验分别对应：

1. `notebook_ablation_no_fno.ipynb`
   移除 Fourier neural operator style preprocessing block，观察没有频域/非局部预处理时模型表现如何。

2. `notebook_ablation_no_attention.ipynb`
   移除 U-Net skip connection 中的 attention gates，观察普通 U-Net skip connection 的表现。

3. `notebook_ablation_no_gradient_loss.ipynb`
   保留模型结构，但训练 loss 中只使用 MSE，不使用 gradient matching loss。

每个消融 notebook 都应尽量保持和完整模型相同的：

- 数据划分方式
- basis function 设置
- batch size
- epoch 数量
- optimizer
- 保存路径结构
- 可视化方式
- 指标记录方式

这样消融结果才可以和完整模型公平比较。

## 5. Use GitHub to Submit Your Work

所有阶段性工作都需要通过 GitHub 提交。建议每完成一个清晰步骤就 commit 一次。

推荐提交内容：

- 修改后的 notebook
- 你的任务记录或实验说明
- 小的 `.csv`、`.json` 指标文件
- 关键可视化图片

不要提交：

- 原始大数据文件
- 很大的模型 checkpoint
- 临时缓存文件
- 密码、token 或私人信息

常用命令：

```bash
git status
git add notebook_full_model.ipynb task1.md
git commit -m "Run full model task setup"
git push
```

如果你新增了三个消融 notebook，可以使用：

```bash
git add notebook_ablation_no_fno.ipynb notebook_ablation_no_attention.ipynb notebook_ablation_no_gradient_loss.ipynb
git commit -m "Add ablation study notebooks"
git push
```

## 6. Using AutoDL for GPU Training

如果本地电脑没有合适的 GPU，可以使用 AutoDL 进行训练。

建议流程：

1. 在 AutoDL 上创建带 GPU 的实例。
2. 通过 GitHub clone 自己 fork 后的仓库。
3. 上传或挂载所需数据文件到 `data/` 目录。
4. 安装或选择包含 PyTorch、NumPy、SciPy、h5py、pandas、matplotlib 和 Jupyter 的环境。
5. 在 AutoDL 中启动 JupyterLab 或 Jupyter Notebook。
6. 先用 `RUN_MODE = "quick"` 测试流程。
7. 再使用 `RUN_MODE = "full"` 做正式训练。
8. 下载需要保存的结果，或把小文件提交回 GitHub。

在 AutoDL 上运行时，也请记录：

- GPU 型号
- Python/PyTorch 环境
- 训练耗时
- 是否使用 CUDA
- 输出文件路径

## 7. Expected Deliverables

第一阶段结束时，你应该提交：

- 跑通过的 `notebook_full_model.ipynb`
- 完整模型的主要结果说明
- 至少一组完整模型的测试指标和可视化结果
- 三个消融研究 notebook 文件
- GitHub commit 记录

谱分析暂时不作为 Task 1 的内容。等完整模型和三个消融模型都完成后，再进入下一阶段的频谱误差分析和跨模型比较。
