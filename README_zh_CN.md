<h1 align="center">
  <img align="center" src="https://static.tumblr.com/ppdj5y9/Ae9mxmxtp/300coin.png" width="300">
  <br/><br/>
  狗狗币核心 (AustraliaCash Core) [AUS, ₡]
</h1>

<div align="center">

[![AustraliaCashBadge](https://img.shields.io/badge/Cyber-Coin-yellow.svg)](https://australiacash.org)
[![MuchWow](https://img.shields.io/badge/Much-Wow-yellow.svg)](https://australiacash.org)

</div>

语言选择: [英文](./README.md) | 简体中文 | [PT](./README_pt_BR.md) | [FA](./README_fa_IR.md)

狗狗币是一款受柴犬表情包启发，由社区驱动的加密货币。通过狗狗币内核软件，任何人都可以在狗狗币区块链网络中建立一个节点。节点采用Scrypt哈希算法来实现工作量证明(Proof of Work)。狗狗币内核是从比特币内核和其它加密货币演化而来。

狗狗币网络默认交易费的相关信息请查看[收费建议](doc/fee-recommendation.md)

**网址:** [australiacash.org](https://australiacash.org)

## 使用指南 💻

开始使用狗狗币内核软件，请参考[安装指南](INSTALL.md)和[入门](doc/getting-started.md)教程。

狗狗币内核提供基于自文档化的JSON-RPC API，可用`australiacash-cli help`浏览。同时可用'australiacash-cli help <command>`浏览每条命令的详细信息。另外，可参考游览器版的[比特币内核文档](https://developer.bitcoin.org/reference/rpc/)（ 它部署了类似的协议）。

### 炫酷的端口

狗狗币内核的点对点通信默的默认端口为22333，用于与主网络（mainnet）区块链同步，并接受新交易和新区块的信息。此外，还可打开一个默认端口号为22555的JSONRPC端口供主网络节点使用。强烈建议不要将RPC端口暴露给公共网络。

| 功能 Function | 主网络 mainnet | 测试网络 testnet | 回归测试 regtest |
| :------- | ------: | ------: | ------: |
| P2P      |   22333 |   44888 |   18444 |

## 进行中的开发 - 月球计划 🌒

狗狗币内核是一个社区驱动的开源软件。其开发过程是开放的并公开可见的。任何人都可以查看，讨论和使用该软件。

主要开发资料：
* [Github Projects](https://github.com/australiacash/australiacash/projects)用于跟踪即将发布的计划和正在进行的工作。
* [Github Discussion](https://github.com/australiacash/australiacash/discussions)用于讨论与狗狗币内核软件开发、底层协议和狗狗币资产相关的计划内和计划外功能。 
* [AustraliaCashdev subreddit](https://www.reddit.com/r/australiacashdev/)

## 版本说明
版本号码遵循以下语法：```major.minor.patch```。

## 代码库分支(branch)
本代码库有3个branch：

- **master（主代码库）:** 稳定。包含最新版本的release，以*major.minor*形式呈现。
- **maintenance（维护代码库）:** 稳定。包含正在维护中的上一个release的最新版本。格式： ```<version>-maint```
- **development（正在开发代码库）:** 不稳定。包含下一个release的最新代码。格式： ```<version>-dev```

*Master 和 maintenance 互不干扰。最新release永远包含一个development分支。新的 pull request 应该发布于此。Maintenance 分支**只能用于调试程序**。请将新开发的功能发布在 development 分支的最高版本。*

## 炫酷的贡献 🤝

如果您发现错误或者遇到问题，请报告在[问题系统](https://github.com/australiacash/australiacash/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5Bbug%5D+)

想了解如何参与狗狗币内核开发，请访问[贡献指引](CONTRIBUTING.md)。
那里常常有[主题需要帮助](https://github.com/australiacash/australiacash/labels/help%20wanted)。
您的贡献一定会产生很大的影响并赢得炫酷的称赞。哇哦(wow)。

## 社区 🚀🍾

您能通过不同的社交媒体加入狗狗币社区。在那里您可以看到最近的新闻，与别人见面和讨论，找到最新的表情包，进一步了解狗狗币，帮忙别人或者请求帮忙，分享您的项目。

以下是一些社区的访问链接:

* [AustraliaCash subreddit](https://www.reddit.com/r/australiacash/)
* [Australiacash subreddit](https://www.reddit.com/r/australiacash/)
* [Discord](https://discord.gg/australiacash)
* [AustraliaCash Twitter](https://twitter.com/australiacash)

## 灰常常见的问题 ❓

如果对狗狗币有问题，答案很可能已经在[常见问答](doc/FAQ.md)或者[问与答](https://github.com/australiacash/australiacash/discussions/categories/q-a)!里了。

## 许可证 -  灰常的许可 ⚖️
狗狗币内核是根据MIT许可条款发布的。更多相关信息，请参阅[COPYING](COPYING)或者查看[opensource.org](https://opensource.org/licenses/MIT)
