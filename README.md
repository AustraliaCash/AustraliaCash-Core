## Australia Cash

Australia Cash is experimental software.

### V3 Security Release

V3 was developed in direct response to the attack vectors discovered in V1 and V2. This release introduces major security upgrades designed to strengthen network integrity and chain stability.

# AustraliaCash-Core
AUS-Cash Core Auxilary Proof Of Work Wallet
v3.7.0.01
####	About

>		Australiacash is a free open source peer-to-peer electronic system that is
>		completely decentralized, without the need for a central server or trusted
>		parties.  Users hold the crypto keys to their own Australia Cash and transact directly
>		with each other, with the help of a peer-to-peer network to check for double-spending.
>
>		Australia Cash is a peer-to-peer cryptocurrency and open-source software project released 
>		under the MIT/X11 license. Creation and transfer of coins is based on an open source 
>		cryptographic protocol and is not managed by any central authority.


>		Australiacash Core is the original Australiacash client and it builds the backbone of the network.
>		However, it downloads and stores the entire history of Australiacash transactions
>		depending on the speed of your computer and network connection, the synchronization
>		process can take anywhere from a few hours to a day or more.		


####    Install Instructions

>       Proceed to the releases section of this GitHub
>       Find the latest release at top of page (Latest 3.7.0.01)
>       Download the compressed file for your operating system
>       Unzip and double click the AustraliaCash-qt file
>
>       Open ports 1986-1987 via the routers port forwarding or virtual server option for better peers connectivity.
>       Start the wallet with australiacash-qt

### Version strategy
Version numbers are following ```major.minor.patch``` semantics.

### Branches
There are 3 types of branches in this repository:

- **master:** Stable, contains the latest version of the latest *major.minor* release.
- **maintenance:** Stable, contains the latest version of previous releases, which are still under active maintenance. Format: ```<version>-maint```
- **development:** Unstable, contains new code for planned releases. Format: ```<version>-dev```

*Master and maintenance branches are exclusively mutable by release. Planned*
*releases will always have a development branch and pull requests should be*
*submitted against those. Maintenance branches are there for **bug fixes only,***
*please submit new features against the development branch with the highest version.*

## Contributing 🤝

If you find a bug or experience issues with this software, please report it
using the [issue system](https://github.com/australiacash/australiacash/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5Bbug%5D+).

Please see [the contribution guide](CONTRIBUTING.md) to see how you can
participate in the development of AustraliaCash Core. There are often
[topics seeking help](https://github.com/australiacash/australiacash/labels/help%20wanted)
where your contributions will have high impact and get very appreciation. wow.

## Communities 🚀🍾

You can join the communities on different social media.
To see what's going on, meet people & discuss, find the latest meme, learn
about AustraliaCash, give or ask for help, to share your project.

Here are some places to visit:

* [AustraliaCash subreddit](https://www.reddit.com/r/australiacash/)
* [Discord](https://discord.gg/UbrF48v43D)
* [AustraliaCash Twitter](https://twitter.com/australiacash)

## Very Much Frequently Asked Questions ❓

Do you have a question regarding AustraliaCash? An answer is perhaps already in the
[FAQ](doc/FAQ.md) or the
[Q&A section](https://github.com/australiacash/australiacash/discussions/categories/q-a)
of the discussion board!
=======
Key protections include:

* Advanced reorganisation (reorg) protection derived from proven techniques implemented in Zcash.
* 20,000 block confirmation requirements for new chain acceptance, significantly reducing the risk of hostile chain attacks and deep reorganisations.
* Additional consensus and validation hardening to protect long-term network security.

To date, the V3 chain remains unaffected by known attacks and has demonstrated strong resilience under current threat models.

Australia Cash remains an experimental project, and security research is always encouraged. We welcome responsible disclosure of bugs, vulnerabilities, or unexpected behaviour through our Discord or here on GitHub.

## License - Much license ⚖️
AustraliaCash Core is released under the terms of the MIT license. See
[COPYING](COPYING) for more information or see
[opensource.org](https://opensource.org/licenses/MIT)
