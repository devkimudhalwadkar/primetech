import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
  CardDescription
} from '@/components/ui/card';

const salesData = [
  {
    name: 'Rahul Sharma',
    email: 'rahul.sharma@email.com',
    avatar: 'https://api.slingacademy.com/public/sample-users/1.png',
    fallback: 'RS',
    amount: '+₹12,999.00',
    course: 'Data Science Certification'
  },
  {
    name: 'Priya Patel',
    email: 'priya.patel@email.com',
    avatar: 'https://api.slingacademy.com/public/sample-users/2.png',
    fallback: 'PP',
    amount: '+₹8,499.00',
    course: 'Web Development Bootcamp'
  },
  {
    name: 'Arjun Singh',
    email: 'arjun.singh@email.com',
    avatar: 'https://api.slingacademy.com/public/sample-users/3.png',
    fallback: 'AS',
    amount: '+₹15,999.00',
    course: 'Full Stack Development'
  },
  {
    name: 'Ananya Gupta',
    email: 'ananya.gupta@email.com',
    avatar: 'https://api.slingacademy.com/public/sample-users/4.png',
    fallback: 'AG',
    amount: '+₹6,999.00',
    course: 'UI/UX Design Masterclass'
  },
  {
    name: 'Vikram Mehta',
    email: 'vikram.mehta@email.com',
    avatar: 'https://api.slingacademy.com/public/sample-users/5.png',
    fallback: 'VM',
    amount: '+₹9,999.00',
    course: 'Machine Learning Fundamentals'
  }
];

export function RecentSales() {
  return (
    <Card className='h-full'>
      <CardHeader>
        <CardTitle>Recent Enrollments</CardTitle>
        <CardDescription>
          You had 265 new course enrollments this month.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className='space-y-8'>
          {salesData.map((sale, index) => (
            <div key={index} className='flex items-center'>
              <Avatar className='h-9 w-9'>
                <AvatarImage src={sale.avatar} alt='Avatar' />
                <AvatarFallback>{sale.fallback}</AvatarFallback>
              </Avatar>
              <div className='ml-4 space-y-1'>
                <p className='text-sm leading-none font-medium'>{sale.name}</p>
                <p className='text-muted-foreground text-sm'>{sale.course}</p>
              </div>
              <div className='ml-auto font-medium'>{sale.amount}</div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
