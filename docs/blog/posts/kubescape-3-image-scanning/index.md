---
date: 2023-10-23
categories:
  - Announcements
  - Project
authors:
  - vladklokun
slug: 'kubescape-3-image-scanning'
---

# Kubescape 3.0: Introducing Image Scanning

In the latest release of Kubescape, we completely overhauled the CLI experience to make it easier and faster for you to improve the security of your clusters.

Watch a short video for a demonstration of image scanning from the Kubescape CLI and its benefits, or read on.

<div class="video-wrapper">
  <iframe width="640" height="360" src="https://youtu.be/rjLL_5F41Oc" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</div>

<!-- more -->

## What’s new and howto?

### Scanning an image in the Kubescape CLI

To scan an image, simply run the following command:

"

kubescape scan image 

"

Kubescape will then scan the image for vulnerabilities and show you the results. 

<figure markdown>
  ![Image scan](image-scan-results.png){ width="600" }
  <figcaption>Result of image vulnerability scanning in Kubescape</figcaption>
</figure>

The results include the following information:

* The most pressing vulnerabilities in the image

* The most vulnerable components

* A link to the documentation for each vulnerability

If you would like to see all of the vulnerabilities, regardless of severity, you can run the command in verbose mode with the -v flag.

"

kubescape scan image  --verbose

"

The initial scan can take a while, as it is a comprehensive scan of everything. Subsequent scans are much quicker, so you can easily scan your images as part of your CI/CD pipeline.

## Adding scans to your CI/CD pipelines

Having said that, the use case for security in CI/CD pipelines is not only about speed. To support this we extended our severity threshold flag to support image scanning. Just indicate the severity you would like to fail on, and Kubescape will fail your runs on them.

"

kubescape scan image my-image:latest --severity-threshold high

"

We believe that image scanning is an essential part of any Kubernetes security strategy. We encourage you to try it out and see for yourself how it can help you keep your images safe.


## Conclusion

Image scanning is key to maintaining a tight security posture. It is now available on Kubescape and can be run via the CLI or embedded into your CI/CD pipelines. To learn more, please visit the [Kubescape documentation](https://kubescape.io/operator/vulnerabilities.md).

Feel free to [raise any issues in the Kubescape GitHub project](https://github.com/kubescape/kubescape/issues) or ask questions [in our Slack channel](https://kubescape.io/project/community/#slack).

Are you enjoying Kubescape? [Please fill in our user survey!](https://kubescape.io/project/survey/)
