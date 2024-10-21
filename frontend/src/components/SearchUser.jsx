import { useState } from "react";
import { Input, Box, FormControl, FormLabel, Button, HStack } from "@chakra-ui/react";
import axios from "axios";
import { BASE_URL } from "../App";

const SearchUser = ({ setUsers }) => {
    const [query, setQuery] = useState("");
    const [isLoading, setIsLoading] = useState(false);  // Add loading state

    const handleSearch = async () => {
        if (!query.trim()) return;  // Ensure query is not empty
        setIsLoading(true);  // Start loading animation

        try {
            const response = await axios.get(`${BASE_URL}/friends/search`, {
                params: { query },  // Pass the single query parameter
            });
            setUsers(response.data);
        } catch (error) {
            console.error("Error fetching friends:", error);
        } finally {
            setIsLoading(false);  // Stop loading animation
        }
    };

    // Search on pressing 'Enter'
    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            handleSearch();
        }
    };

    return (
        <Box mb={6} p={4} shadow="md" borderWidth="1px" borderRadius="lg" textAlign="center">
            <FormControl id="search">
                <FormLabel textAlign="center" fontSize="xl" mb={4}>
                    Search by Name or Role
                </FormLabel>

                {/* Search input and button in a horizontal stack */}
                <HStack justifyContent="center" spacing={4}>
                    <Input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        onKeyDown={handleKeyDown}  // Trigger search on Enter key
                        placeholder="Enter name or role"
                        focusBorderColor="cyan.400"
                        maxW="400px"
                    />
                    <Button
                        onClick={handleSearch}
                        colorScheme="cyan"
                        variant="solid"
                        isLoading={isLoading}
                    >
                        Search
                    </Button>
                </HStack>
            </FormControl>
        </Box>
    );
};

export default SearchUser;
