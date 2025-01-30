import Link from "next/link";

const Footer = () => {
    return (
        <footer className="w-full bg-white shadow-md mt-10 py-6 text-center">
            <p className="text-gray-600">© {new Date().getFullYear()} ChatWithDocs. All rights reserved.</p>
            <div className="mt-2 space-x-4">
                <Link href="/terms" className="text-gray-500 hover:text-gray-900">Terms</Link>
                <Link href="/privacy" className="text-gray-500 hover:text-gray-900">Privacy</Link>
            </div>
        </footer>
    );
};

export default Footer;
