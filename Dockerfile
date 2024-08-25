FROM debian:stable-slim AS builder
RUN apt-get update
RUN apt-get install -y bsdmainutils build-essential cargo clang git
WORKDIR /usr
RUN git clone --depth 1 https://github.com/romanz/electrs.git
RUN cd electrs && cargo install --config net.git-fetch-with-cli=true --locked --path .
FROM debian:stable-slim AS runner
WORKDIR /usr/app
RUN apt-get update
RUN apt-get install -y librocksdb-dev
COPY --from=builder /root/.cargo/bin/electrs /usr/app/electrs
ENTRYPOINT ["/usr/app/electrs"]
