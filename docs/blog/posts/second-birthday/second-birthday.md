---
draft: false 
date: 2023-09-14
categories:
  - Announcements
  - Project
authors:
  - slashben
---

# Happy second birthday, Kubescape!

What do you get a piece of software for its second birthday?  A brand-new blog, of course! And cake.  More on the cake later.

Kubescape is an open-source Kubernetes security platform that helps you identify and fix security risks, misconfigurations and vulnerabilities in your Kubernetes clusters. It is a powerful tool that can save you time and effort, and help you keep your Kubernetes deployments secure.

<!-- more -->

I co-founded ARMO, the creators of Kubescape, with the idea of bringing runtime security to Kubernetes deployments. As security engineers, we went to CISOs and security teams at enterprises and asked them what they needed. They told us that the Kubernetes deployments were the responsibility of the DevOps teams, and we should go talk to them.

The DevOps teams we spoke to had a whole different set of problems than the one we set out to solve. They were concerned by the hundreds of configuration options available in Kubernetes. They wanted tools to manage their security posture, reduce the amount of work to engineer and validate secure applications, and validate that their environments were compliant with industry best practices. They also emphasized the importance of these tools being available for immediate download, being open source, and being part of the larger Cloud Native community.

We heard you loud and clear, and in September 2021 we launched Kubescape.  That means we’re now two years old!

The [initial version of Kubescape](https://www.cncf.io/blog/2021/09/03/kubescape-the-first-open-source-tool-for-running-nsa-and-cisa-kubernetes-hardening-tests/) let you validate your cluster against the then-recently published NSA and CISA Kubernetes hardening guidelines. Further releases added [support for the MITRE ATT&CK framework](https://www.businesswire.com/news/home/20211012005814/en/ARMO-Launches-Expanded-Version-of-Kubescape-World%E2%80%99s-First-Open-Source-Kubernetes-Testing-Tool-Compliant-with-NSA-CISA-Hardening-Guidance) and [CIS benchmarks](https://www.prnewswire.com/il/news-releases/armo-adds-cis-benchmark-to-kubescape-to-boost-kubernetes-security-and-compliance-scanning-301660019.html), and the security library now includes over 230 controls to validate your security posture.

We also added support for vulnerability scanning, allowing you to check for CVEs in your running containers or in a container registry, and recently added a [capability to help users prioritize vulnerability detection by using eBPF to detect which packages are loaded at runtime](https://www.armosec.io/blog/kubernetes-vulnerability-relevancy-and-prioritization/).

[Kubescape joined the Cloud Native Computing Foundation (CNCF)](https://www.armosec.io/blog/cncf-accepts-kubescape-security-and-compliance-scanner/) in December 2021, becoming the first and only open source, CNCF-hosted tool for [Kubernetes security posture management](https://www.armosec.io/glossary/kubernetes-security-posture-management/). With almost 9,000 stars in GitHub, and users doing almost a million scans per month, it has become one of the most popular tools in this space.

ARMO has bet its business on open source, offering a [comprehensive Kubernetes security platform](https://cloud.armosec.io/) powered by Kubescape. However, this same engine is available to anyone, and we’re delighted to see [companies like Jit building their Kubernetes support on top of Kubescape.](https://www.jit.io/blog/kubescape-jit)

Oh, and did we mention cake?  The ARMO team celebrated Kubescape's second birthday by decorating some cakes.  Congratulations to [Amir](https://github.com/amirmalka), [Yiscah](https://github.com/YiscahLevySilas1) and [Rina](https://github.com/RinaO1234), our winning team.

<figure class="video_container">
  <video controls="false" allowfullscreen="true" loop="true" autoplay="true">
    <source src="/blog/second-birthday/cakes.mp4" type="video/mp4">
  </video>
</figure>

We are excited to tell you about some of the new features in our upcoming version. Keep an eye on our new blog in the next few days.
