/**
 * Apply the greedy algorithm to calculate coin change.
 * @param amount a non-negative integer which is required to be made up.
 * @param denominations the available coin types (unique positive integers)
 * @return a map of each denomination to the number of times it is used in the solution.
 * **/

public static Map<Integer,Integer> greedyChange(int amount, int[] denominations){
        Arrays.sort(denominations);
        int n = denominations.length;
Map<Integer, Integer> result = new HashMap<>();
        for (int denomination : denominations) {
            result.put(denomination, 0);
        }
            for (int i = n - 1; i >= 0; i--) {
            int denomination = denominations[i];
            int numCoins = amount / denomination;
            amount = amount % denomination;
            result.put(denomination, numCoins);
        }

        return result;        
}


/**
 * Apply the greedy algorithm to calculate coin change.
 * @param amount a non-negative integer which is required to be made up.
 * @param denominations the available coin types (unique positive integers)
 * @return a map of each denomination to the number of times it is used in the solution.
 * **/

public static Map<Integer,Integer> greedyChange(int amount, int[] denominations){
Arrays.sort(denominations);
        int n = denominations.length;
Map<Integer, Integer> result = new HashMap<>();

        assert loopInvariant(amount, denominations, result);

        for (int denomination : denominations) {
            result.put(denomination, 0);
        }
            for (int i = n - 1; i >= 0; i--) {
            int denomination = denominations[i];
            int numCoins = amount / denomination;
            amount = amount % denomination;
            result.put(denomination, numCoins);
            assert loopInvariant(amount, denominations, result);
            
        }

        return result;         
    
}
        
public static boolean loopInvariant(int amount, int[] denominations, Map<Integer, Integer> result){
    
        int totalValue = 0;
        for (int denomination : denominations) {
            totalValue += denomination*result.get(denomination);
        }

        if (totalValue != amount) {
            return false;
        }

        for (int coinCount : result.values()) {
            if (coinCount < 0) {
                return false;
            }
        }
        return true;
}


public static Map<Integer,Integer> exactChange(int amount, int[] denominations){
        
        Arrays.sort(denominations);
        int n = denominations.length;

        int[] dp = new int[amount + 1];
        Arrays.fill(dp, Integer.MAX_VALUE);
        dp[0] = 0;

        int[][] chosenCoins = new int[amount + 1][n];
        Arrays.fill(chosenCoins[0], 0);

        for (int i = 1; i <= amount; i++) {
            for (int j = 0; j < n; j++) {
                if (denominations[j] <= i) {
                    int subProblem = dp[i - denominations[j]];
                    if (subProblem != Integer.MAX_VALUE && subProblem + 1 < dp[i]) {
                        dp[i] = subProblem + 1;
                        System.arraycopy(chosenCoins[i - denominations[j]], 0, chosenCoins[i], 0, n);
                        chosenCoins[i][j]++;
                    }
                }
            }
        }

        Map<Integer, Integer> result = new HashMap<>();
        for (int i = 0; i < n; i++) {
            result.put(denominations[i], chosenCoins[amount][i]);
        }

        return result;       
}