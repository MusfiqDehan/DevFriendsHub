import {
	Button,
	Flex,
	FormControl,
	FormLabel,
	Input,
	Modal,
	ModalBody,
	ModalCloseButton,
	ModalContent,
	ModalFooter,
	ModalHeader,
	ModalOverlay,
	Radio,
	RadioGroup,
	Textarea,
	useDisclosure,
	useToast,
} from "@chakra-ui/react";
import { useState } from "react";
import { BiAddToQueue } from "react-icons/bi";
import { BASE_URL } from "../App";

const CreateUserModal = ({ setUsers }) => {
	const { isOpen, onOpen, onClose } = useDisclosure();
	const [isLoading, setIsLoading] = useState(false);
	const [inputs, setInputs] = useState({
		name: "",
		role: "",
		description: "",
		gender: "",
	});
	const [image, setImage] = useState(null);
	const [imagePreview, setImagePreview] = useState(null);
	const toast = useToast();

	const handleImageChange = (e) => {
		const file = e.target.files[0];
		if (file) {
			setImage(file);
			setImagePreview(URL.createObjectURL(file));
		}
	};

	const handleCreateUser = async (e) => {
		e.preventDefault(); // prevent page refresh
		setIsLoading(true);
		try {
			const formData = new FormData();
			formData.append("name", inputs.name);
			formData.append("role", inputs.role);
			formData.append("description", inputs.description);
			formData.append("gender", inputs.gender);
			if (image) {
				formData.append("image_upload", image);
			}

			const res = await fetch(BASE_URL + "/friends", {
				method: "POST",
				body: formData,
			});

			const data = await res.json();
			if (!res.ok) {
				throw new Error(data.error);
			}

			toast({
				status: "success",
				title: "Yayy! 🎉",
				description: "Friend created successfully.",
				duration: 2000,
				position: "top-center",
			});
			onClose();
			setUsers((prevUsers) => [...prevUsers, data]);

			setInputs({
				name: "",
				role: "",
				description: "",
				gender: "",
			}); // clear inputs
			setImage(null);
			setImagePreview(null);
		} catch (error) {
			toast({
				status: "error",
				title: "An error occurred.",
				description: error.message,
				duration: 4000,
			});
		} finally {
			setIsLoading(false);
		}
	};

	return (
		<>
			<Button onClick={onOpen}>
				<BiAddToQueue size={20} />
				Add New Friend
			</Button>

			<Modal isOpen={isOpen} onClose={onClose}>
				<ModalOverlay />
				<form onSubmit={handleCreateUser}>
					<ModalContent>
						<ModalHeader> Add New Friend </ModalHeader>
						<ModalCloseButton />

						<ModalBody pb={6}>
							<Flex alignItems={"center"} gap={4}>
								{/* Left */}
								<FormControl>
									<FormLabel>Full Name</FormLabel>
									<Input
										placeholder='John Doe'
										value={inputs.name}
										onChange={(e) => setInputs({ ...inputs, name: e.target.value })}
									/>
								</FormControl>

								{/* Right */}
								<FormControl>
									<FormLabel>Role</FormLabel>
									<Input
										placeholder='Software Engineer'
										value={inputs.role}
										onChange={(e) => setInputs({ ...inputs, role: e.target.value })}
									/>
								</FormControl>
							</Flex>

							<FormControl mt={4}>
								<FormLabel>Description</FormLabel>
								<Textarea
									resize={"none"}
									overflowY={"hidden"}
									placeholder="He's a software engineer who loves to code and build things."
									value={inputs.description}
									onChange={(e) => setInputs({ ...inputs, description: e.target.value })}
								/>
							</FormControl>

							<RadioGroup mt={4}>
								<Flex gap={5}>
									<Radio
										value='male'
										onChange={(e) => setInputs({ ...inputs, gender: e.target.value })}
									>
										Male
									</Radio>
									<Radio
										value='female'
										onChange={(e) => setInputs({ ...inputs, gender: e.target.value })}
									>
										Female
									</Radio>
								</Flex>
							</RadioGroup>

							<FormControl mt={4}>
								<FormLabel>Upload Image</FormLabel>
								{imagePreview && <img src={imagePreview} alt="Preview" style={{ marginBottom: '10px', maxWidth: '100%' }} />}
								<Input type="file" accept="image/*" onChange={handleImageChange} />
							</FormControl>
						</ModalBody>

						<ModalFooter>
							<Button colorScheme='blue' mr={3} type='submit' isLoading={isLoading}>
								Add
							</Button>
							<Button onClick={onClose}>Cancel</Button>
						</ModalFooter>
					</ModalContent>
				</form>
			</Modal>
		</>
	);
};
export default CreateUserModal;