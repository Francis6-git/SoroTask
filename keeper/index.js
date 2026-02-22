const config = require('./src/config');
const { server } = require('./src/rpc');
const { Keypair } = require('@stellar/stellar-sdk');
const { initializeKeeperAccount } = require('./src/account');
const ExecutionQueue = require('./src/queue');

async function main() {
    console.log("Starting SoroTask Keeper...");
    console.log(`Configured for network: ${config.networkPassphrase}`);
    console.log(`RPC URL: ${config.rpcUrl}`);

    let keeperData;
    try {
        keeperData = await initializeKeeperAccount();
    } catch (err) {
        console.error(`Failed to initialize keeper: ${err.message}`);
        process.exit(1);
    }

    const { keypair, accountResponse } = keeperData;
    const queue = new ExecutionQueue();

    try {
        // Connection validation / Startup health check
        const networkInfo = await server.getNetwork();
        console.log("Successfully connected to Soroban RPC!");
        console.log("Network Passphrase from RPC:", networkInfo.passphrase);

        if (networkInfo.passphrase !== config.networkPassphrase) {
            throw new Error(`Network passphrase mismatch! Expected: ${config.networkPassphrase}, Got: ${networkInfo.passphrase}`);
        }
    } catch (err) {
        console.error("Failed to connect to Soroban RPC or network mismatch:", err.message);
        process.exit(1);
    }

    // Polling loop
    const pollingInterval = setInterval(async () => {
        console.log("Checking for due tasks...");
        // TODO: Query contract for tasks due for execution

        // Mocking some due tasks to test enqueue
        // const dueTaskIds = await getDueTasks();
        // await queue.enqueue(dueTaskIds, dummyExecutor);

    }, config.pollingIntervalMs);
}

main().catch(err => {
    console.error("Keeper initialization failed:", err);
    process.exit(1);
});

