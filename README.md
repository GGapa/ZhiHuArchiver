# 介绍

本项目用于个人下载自己在知乎上的所有回答和文章，并生成一个简单的站点展示。成果见此：https://ggapa.github.io/ZhiHuArchive/

# 如何使用？

Fork 该仓库至你的账户下，将仓库名更改为你喜欢的名字，当然保持不变也是没有问题的。

接着，获取你的知乎 Cookie，并根据 `.env.example` 配置你自己的 `.env`，然后根据提示修改并配置 `.github/workflows/build-and-deploy.yml`

配置好后，在终端中运行 `update.py`。

```
python update.py
```

等待下载。在下载结束后，push 至 Github 上，启用 Github Action 即可，稍等片刻，你便可以在 `[你的用户名].github.io/[你的仓库名]` 中看到你的知乎备份了。

# 致谢

本项目灵感来源于 [L-M-Sherlock/ZhiHuArchive](https://github.com/L-M-Sherlock/ZhiHuArchive)，非常感谢开发者的辛勤付出。
