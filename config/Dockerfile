FROM python:3.9

WORKDIR /aiops

# set display port
ENV DISPLAY=:99

# install ansible, kubernetes, selenium, google chrome, unzip, chromedriver, helm, kubectl, kustomize, oc
RUN pip install ansible \
    kubernetes \
    jmespath \
    selenium && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt -y update && \
    apt install -y google-chrome-stable \
    unzip && \
    wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    wget -q https://get.helm.sh/helm-v3.6.3-linux-amd64.tar.gz && \
    tar -xzf helm-v3.6.3-linux-amd64.tar.gz && \
    mv linux-amd64/helm /usr/local/bin && \
    rm -rf linux-amd64 helm-v3.6.3-linux-amd64.tar.gz && \
    # wget https://self-hosted.instana.io/kubectl/kubectl-instana-darwin_amd64-release-243-0.tar.gz && \
    # tar xfzv kubectl-instana-darwin_amd64-release-243-0.tar.gz && \
    # mv kubectl-instana /usr/local/bin/kubectl-instana && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s  https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/ && \
    curl -s "https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh" | bash && \
    mv kustomize /usr/local/bin/ && \
    wget -O /usr/local/bin/oc "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/latest/openshift-client-linux.tar.gz" && \
    tar xvzf /usr/local/bin/oc -C /usr/local/bin/ oc && \
    chmod +x /usr/local/bin/oc

COPY ./ ./.dockerignore ./

# configure kubectl-instana
RUN mv ./kubectl-instana /usr/bin/

# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["ansible-playbook", "aiops-accelerator.yaml"]