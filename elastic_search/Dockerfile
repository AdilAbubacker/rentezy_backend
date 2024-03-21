FROM docker.elastic.co/elasticsearch/elasticsearch:8.5.1

# Set ulimits
RUN ulimit -u 4096

# Set JVM options
ENV ES_JAVA_OPTS="-Xms1g -Xmx4g"
