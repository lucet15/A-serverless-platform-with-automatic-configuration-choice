deployment da app.js num cluster criado na aws

affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values:
                      - t2.medium

nesta parte, é selecionada o instance type especifico
