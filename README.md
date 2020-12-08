![](./architecture.jpg?raw=true "SWEETEN Architecture")

# SWEETEN
## aSsistant for netWork managEmEnT of microsErvices-based VNFs

This is a prototype for the work proposed in the paper "[SWEETEN: Automated Network Management Provisioning for 5G Microservices-Based Virtual Network Functions](https://ieeexplore.ieee.org/abstract/document/9269063), presented in CNSM 2020. If you want to cite this work, please do so using the following bib entry:

<pre>
    <code>
  @inproceedings{de2020sweeten,
  title={SWEETEN: Automated Network Management Provisioning for 5G Microservices-Based Virtual Network Functions},
  author={de Jesus Martins, Rafael and Dalla-Costa, Ariel Galante and Wickboldt, Juliano Araujo and Granville, Lisandro Zambenedetti},
  booktitle={2020 16th International Conference on Network and Service Management (CNSM)},
  pages={1--9},
  year={2020},
  organization={IEEE}
  }
    </code>
</pre>

### Instructions
0. Augment the yaml deployment specification with management feature requests for desired Deployment/Services (limited at this time; try "monitoring: flows" as management feature request)
0.b. Along with the main request, additional parameters can be included in the specification. SWEETEN will try to use them when determining the tools/configuration for the deployment. Any remaining option will be passed on to the management container as environment variables (so that users can alter low-level parameters "directly" through the specification); these variables may be ignored by the container
1. Use the augmented yaml as input for SWEETEN (e.g., sweeten input/input.yaml)
2. The system will generate the output file and will attempt to deploy it in a Kubernetes cluster (through kubectl)
2.b. Output yaml file can be found in the "solution" folder
3. SWEETEN will return to the user the URL for a dashboard that monitors their Deployments (according to what was specified in step 0)
